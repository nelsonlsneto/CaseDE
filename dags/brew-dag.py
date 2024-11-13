from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import requests
import json
import math
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from airflow.utils.email import send_email

# Function to send failure emails
def failure_email(context):
    task_instance = context['task_instance']
    task_status = 'Failed'
    subject = f'Airflow Task {task_instance.task_id} {task_status}'
    body = f'The task {task_instance.task_id} completed with status : {task_status}. \n\n'\
        f'The task execution date is: {context["execution_date"]}\n'\
        f'Log url: {task_instance.log_url}\n\n'
    to_email = 'nelsonlsn@gmail.com'
    send_email(to = to_email, subject = subject, html_content = body)

# Function to test de connection to API
def connect_api():
    url = 'https://api.openbrewerydb.org/v1/breweries/meta'
    response = requests.get(url)
    status_api = response.status_code
    return status_api

def e_valido(ti):
    status_api = ti.xcom_pull(task_ids = 'connect_api')
    if status_api == 200:
        return 'valido'
    return 'nvalido'

# Function to copy the data from API to bronze layer
def copy_from_api():
    url = 'https://api.openbrewerydb.org/v1/breweries/meta'
    response = requests.request("GET", url = url)
    num_brew = int(response.json()['total'])
    num_req = math.ceil((num_brew/200))
    list_brew = []
    for i in range(0, num_req + 1):
        url = f'https://api.openbrewerydb.org/v1/breweries?page={i}&per_page=200'
        response = requests.request("GET", url = url)
        list_brew.extend(response.json())
    return list_brew

def api_bronze(ti):
    list_brew = ti.xcom_pull(task_ids = 'copy_from_api')
    with open("/opt/airflow/datalake/bronze/raw.json", "w") as outfile:
        json.dump(list_brew, outfile)

# Function to copy the data from bronze layer to silver layer
def bronze_silver():
    df_bl = pd.read_json("/opt/airflow/datalake/bronze/raw.json")
    df_bl = df_bl.drop_duplicates()
    df_bl.to_parquet("/opt/airflow/datalake/silver/breweries", partition_cols = 'country', index = False, existing_data_behavior='delete_matching')

default_arguments = {
    "execution_timeout": datetime.timedelta(minutes=30),
    "retry_delay": datetime.timedelta(minutes=1),
    'email_on_failure': True,
    'email': 'nelsonlsn@gmail.com',
    "retries": 1
}

with DAG('brew-dag', default_args=default_arguments, start_date = datetime.datetime(2024,11,11), schedule_interval='0 7 * * *', catchup=False) as dag:

    connect_api = PythonOperator(
        task_id = 'connect_api',
        python_callable = connect_api,
        on_failure_callback = failure_email
    )

    e_valido = BranchPythonOperator(
        task_id = 'e_valido',
        python_callable = e_valido,
        on_failure_callback = failure_email
    )

    valido = BashOperator(
        task_id = 'valido',
        bash_command = "echo 'API valida'",
        on_failure_callback = lambda context: failure_email(context)
    )

    nvalido = BashOperator(
        task_id = 'nvalido',
        bash_command = "echo 'API nao valida'",
        on_failure_callback = lambda context: failure_email(context)
    )

    copy_from_api = PythonOperator(
        task_id = 'copy_from_api',
        python_callable = copy_from_api,
        on_failure_callback = failure_email
    )

    api_bronze = PythonOperator(
        task_id = 'api_bronze',
        python_callable = api_bronze,
        on_failure_callback = failure_email
    )

    bronze_silver = PythonOperator(
        task_id = 'bronze_silver',
        python_callable = bronze_silver,
        on_failure_callback = failure_email
    )

    # Define tasks dependencies
    connect_api >> e_valido >> [valido, nvalido]
    valido >> copy_from_api >> api_bronze >> bronze_silver
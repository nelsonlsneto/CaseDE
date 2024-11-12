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

with DAG('brew-dag', start_date = datetime.datetime(2024,11,11), schedule_interval='30 * * * *', catchup=False) as dag:

    connect_api = PythonOperator(
        task_id = 'connect_api',
        python_callable = connect_api
    )

    e_valido = BranchPythonOperator(
        task_id = 'e_valido',
        python_callable = e_valido
    )

    valido = BashOperator(
        task_id = 'valido',
        bash_command = "echo 'API valida'"
    )

    nvalido = BashOperator(
        task_id = 'nvalido',
        bash_command = "echo 'API nao valida'"
    )


    connect_api >> e_valido >> [valido, nvalido]
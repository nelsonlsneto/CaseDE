# DE CASE INSTRUCTIONS

This case is about retrieving data from an API endpoint, transforming them and taking them through bronze, silver and gold layers.
In this case I used Airflow for orchestration, Docker for modularization and Python as language.

The pipeline was designed to run daily at 07:00 AM. Hence, there is a timeout set to 30 minutes, only 1 retry is set with 1 minute between retries, and Airflow will send an e-mail if the pipeline fails.

First of all, the pipeline will test if the connection with API endpoint is valid or not. Being valid, the pipeline will retrieve data from this endpoint and check if the number of breweries is ok or not (since there is a total of 8355 breweries, I set at least 8000 breweries as ok).
Being ok, the pipeline will copy data through bronze, silver and gold layers.

![pipeline](https://github.com/user-attachments/assets/4887d7e9-dd8d-4b61-b586-1da6e0c53998)


## 1) Preparation

Before we begin, you have to install the following applications on your PC:
1) [Python](https://www.python.org/downloads/)
2) [Docker](https://www.docker.com/products/docker-desktop/)
3) An IDE software of your preference. I used [Visual Studio Code](https://code.visualstudio.com/)

## 2) Clone this repository on your PC

### 2.1) Make sure all these folders exist:
- config
- dags
- datalake
- logs
- plugins

### 2.2) Edit the docker-compose.yaml file with your e-mail credentials:
- Open the docker-compose.yaml file;
- Edit this file with your e-mail credentials. In my case I used Gmail. If you use 2FA, you can create an app password. To do so, you can follow these steps in this [link](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237)
![email](https://github.com/user-attachments/assets/be27b89f-0ff0-45fb-833d-447510f07e98)

### 2.3) After you have edited the docker-compose.yaml file, you have to set Docker up:
- Open Docker;
- Open CMD (Windows);
- Access the folder where this repository was cloned;
- Enter this code on CMD: docker-compose up airflow-init
- Wait until the environment is set;
- Enter this code on CMD: docker-compose up

### 2.4) After you have done these instructions, you will be able to access Airflow:
- Open your browser and open [Airflow](http://localhost:8080/)
- Username: Airflow
- Password: Airflow

## 3) Running your DAG

You can now open the DAG called "brew-dag" and run it by clicking in this yellow button
![dag](https://github.com/user-attachments/assets/5ba907f3-2f8c-4ba7-bc75-e66aec4bef98)

## 4) Shutting down Docker

After you have done evertything, you can shut docker down by entering this code on CMD:
- Access the folder where this repository was cloned;
- Enter this code on CMD: docker-compose down

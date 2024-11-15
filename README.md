# DE CASE INSTRUCTIONS

This case is about retrieving data from an API endpoint, transforming them and taking them through bronze, silver and gold layers.
In this case I used Airflow for orchestration, Docker for modularization and Python as language.

The pipeline was designed to run daily at 07:00 AM. Hence, there is a timeout set to 30 minutes, only 1 retry is set with 1 minute between retries, and Airflow will send an e-mail if the pipeline fails.

First of all, the pipeline will test if the connection with API endpoint is valid or not. Being valid, the pipeline will retrieve data from this endpoint and check if the number of breweries is ok or not (since there are a total of 8355 breweries, I set at least 8000 breweries as ok).
Being ok, the pipeline will copy data through bronze, silver and gold layers.

## 1) Preparation

Before we begin, you have to install the following applications on your PC:
1) [Python](https://www.python.org/downloads/)
2) [Docker](https://www.docker.com/products/docker-desktop/)
3) An IDE software of your preference. I used [Visual Studio Code](https://code.visualstudio.com/)

## 2) Clone this repository on your PC

After you have cloned this repository on your pc, you have to set Docker up:
- Open Docker;
- Open CMD (Windows);
- Access the folder where this repository was cloned;
- Enter this code on CMD: docker-compose up airflow-init
- Wait until the environment is set;
- Enter this code on CMD: docker-compose up

After you have done these instructions, you will be able to access Airflow:
- Open your browser and open [Airflow](http://localhost:8080/)
- Username: Airflow
- Password: Airflow

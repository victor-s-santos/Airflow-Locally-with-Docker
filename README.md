# Running AIRFLOW 2.5.1 Locally

## How to
* 1. Clone this repository:
    - 1.1 git clone: 

* 2. Export env
        - 2.1 Run the following line to create .env file:
            - echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

* 3. Initialize the Airflow instance:
        - 3.1 docker-compose up airflow-init
        - 3.2 docker-compose up

* 4. Access Airflow Server:
    * 4.1 After some minutes, the Airflow server will be available in your localhost accessing the following url: http://localhost:8080/

    * 4.2 Login using the default credentials in docker-compose.yaml file: 
        - Username: airflow
        - Password: airflow

## Acess the Airflow from restapi
* 1. To get the list of your current dags and its status, run the following line (in my case, I am using the default credentials):
    - curl -X GET --user "airflow:airflow" "http://localhost:8080/api/v1/dags"
    
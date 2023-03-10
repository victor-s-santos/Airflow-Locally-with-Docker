from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from tasks.users import _process_user, _store_user, _insert_in_mongo
from datetime import datetime
import json


with DAG(dag_id='processing', start_date=datetime(2022, 1, 1), 
        schedule_interval='@daily', catchup=False) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """
    )

    is_api_avaliable = HttpSensor(
        task_id="is_api_available",
        http_conn_id="user_api",
        endpoint="api/"
    )

    extract_user_info = SimpleHttpOperator(
        task_id="extract_user_info",
        http_conn_id="user_api",
        endpoint="api/",
        method="GET",
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    process_user = PythonOperator(
        task_id="process_user",
        python_callable=_process_user
    )

    store_user = PythonOperator(
        task_id="store_user",
        python_callable=_store_user
    )

    insert_in_mongo = PythonOperator(
        task_id="insert_in_mongo",
        python_callable=_insert_in_mongo
    )

    create_table >> is_api_avaliable >> extract_user_info >> process_user >> store_user >> insert_in_mongo
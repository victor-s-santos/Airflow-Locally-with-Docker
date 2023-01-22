from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime

with DAG('processing', start_date=datetime(2023, 1, 22), 
    schedule_interval='@daily', catchup=False) as dag:

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres",
        sql=""""
        CREATE TABLE IF NOT EXISTS users (
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
        )
        """
    )
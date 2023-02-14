import json
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pandas import json_normalize
from pymongo import MongoClient

def _process_user(ti):
    user = ti.xcom_pull(task_ids="extract_user_info")
    user = user["results"]
    processed_user = json_normalize({
        "first_name": user[0]["name"]["first"],
        "last_name": user[0]["name"]["last"],
        "username": user[0]["login"]["username"],
        "password": user[0]["login"]["password"],
        "email": user[0]["email"]
    })
    processed_user.to_csv("/tmp/processed_user.csv", index=None, header=False)


def _store_user():
    hook = PostgresHook(
        postgres_conn_id="postgres",
    )
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ','",
        filename="/tmp/processed_user.csv"
    )

def _insert_in_mongo(ti):
    print("Inserindo dados no mongo")
    local_client = MongoClient("mongodb://172.18.0.4:27017/")
    #para pegar o valor do localhost, dar um inspect no container do mongo
    db_name = local_client["local_database"]

    db_name["backup"].insert_one({"status": "Enviado com sucesso!"})
    print(f"The user has been inserted in mongodb!")

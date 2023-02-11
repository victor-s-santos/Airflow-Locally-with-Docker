import json
from pandas import json_normalize

def process_user(ti):
    user = ti.xcom_pull(task_ids="extract_user")
    user = user["results"][0]
    processed_user = json_normalize({
        "first_name": user["name"]["first"],
        "last_name": user["name"]["last"],
        "username": user["login"]["username"],
        "password": user["user"]["password"],
        "email": user["email"]
    })
    process_user.to_csv("/tmp/processed_user.csv", index=None, header=False)
from airflow import DAG
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime


ssh_hook = SSHHook(
    remote_host='spark-master',
    port=22,
    username='root',
    key_file='./config/id_ed25519',
    cmd_timeout=None
)


with DAG(
    'hello_ssh',
    description='Hello, World!',
    schedule_interval=None,
    start_date=datetime(2023, 3, 22),
    catchup=False
) as dag:

    hell_wolrd = SSHOperator(
        task_id='hello_world',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh hello-world.py'
    )

    # Define the task dependencies
    # mysql_to_s3_bronze_csv
    # mysql_to_s3_bronze_parquet >> s3_bronze_to_s3_silver
    
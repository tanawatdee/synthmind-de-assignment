from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime


# ===
# DAG
# ===
ssh_hook = SSHHook(
    remote_host='spark-master',
    port=22,
    username='root',
    key_file='./config/demo_sshkey',
    cmd_timeout=None
)

with DAG(
    'poc_key_topics',
    description='POC Key Topics',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 12),
    catchup=False,
    concurrency=1,
    max_active_runs=1 # due to resources limitation (not enough RAM)
) as dag:
    op_poc_key_topics_en = SSHOperator(
        task_id='poc_key_topics_en',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh poc_key_topics_en.py --date {{ds}}'
    )
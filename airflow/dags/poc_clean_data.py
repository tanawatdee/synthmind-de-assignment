from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from datetime import timedelta
import os
import json
import csv
from time import sleep

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
    'poc_clean_data',
    description='POC Clean data',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 12),
    catchup=False,
    max_active_runs=1 # due to resources limitation (not enough RAM)
) as dag:
    op_poc_clean_data_1 = SSHOperator(
        task_id='poc_clean_data_1',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh poc_clean_data_1.py --date {{ds}}'
    )

    op_poc_clean_data_2 = SSHOperator(
        task_id='poc_clean_data_2',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh poc_clean_data_2.py --date {{ds}}'
    )

    op_poc_clean_data_3 = SSHOperator(
        task_id='poc_clean_data_3',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh poc_clean_data_3.py --date {{ds}}'
    )

    op_poc_clean_data_4 = SSHOperator(
        task_id='poc_clean_data_4',
        ssh_hook=ssh_hook,
        command='/opt/spark/submit.sh poc_clean_data_4.py --date {{ds}}'
    )

    # op_poc_clean_data_1 >> op_poc_clean_data_2 >> op_poc_clean_data_3 >> op_poc_clean_data_4
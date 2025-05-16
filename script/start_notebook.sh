#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

cd "$SWD/../airflow"

docker exec -it da-spark-master jupyter notebook --allow-root --ip 0.0.0.0 --port 8888
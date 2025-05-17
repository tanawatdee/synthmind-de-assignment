#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

cd "$SWD/../airflow"

[ ! -z "$1" ] || exit 64

docker exec da-spark-master ./submit.sh $1
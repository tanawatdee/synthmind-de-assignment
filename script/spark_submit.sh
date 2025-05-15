#!/bin/bash

PWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

cd "$PWD/../spark-cluster"

[ ! -z "$1" ] || exit 64

docker exec da-spark-master ./submit.sh $1
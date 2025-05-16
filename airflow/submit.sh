#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

cd "$SWD"
echo $SWD

set -a
. ./conf/.env
set +a

/opt/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/spark/apps/$1 $@

exit $?
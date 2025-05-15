#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

# ===
# Include logger
# ===
. $SWD/logger.sh

clean_old_log
clean_old_tmp

module_file="$(basename $0)"
module_name="run.${module_file:4:-3}"

printbox "Run $module_name"

# ===
# Run
# ===
cd "$SWD/../src"
set -a
. ../.env
set +a

printi "python -m \"$module_name\" $@"
python -m "$module_name" $@

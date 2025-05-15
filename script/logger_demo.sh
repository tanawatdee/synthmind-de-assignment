#!/bin/bash

#      _
#     | |    ___   __ _  __ _  ___ _ __
#     | |   / _ \ / _` |/ _` |/ _ \ '__|
#     | |__| (_) | (_| | (_| |  __/ |
#     |_____\___/ \__, |\__, |\___|_|
#                 |___/ |___/

SCRIPT_PATH="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

. $SCRIPT_PATH/logger.sh

clean_old_log
clean_old_tmp

echo test_printfile > $SCRIPT_PATH/logger_demo_file.txt

print test_print
printi test_printi
printw test_printi
printe test_printe
printfile $SCRIPT_PATH/logger_demo_file.txt
printl key1 val1 key2 val2
printh "an awesome header" "that support multiline"
printhr
print
print "$(create_tmp_file insert_hive sql)"
exit_ok

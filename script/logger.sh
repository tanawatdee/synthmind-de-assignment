#!/bin/bash

# ==============================================================
# AUTHOR        : Tanawat Deepo
# CREATE DATE   : 2021-02-24
# PURPOSE       : General purpose logger
# SPECIAL NOTES : This script should be imported by using
#                 "source" (or ".") command
# ==============================================================
# CHANGE HISTORY:
# Date          Version     Author              Description
# 2021-02-24    1.0.0       Tanawat Deepo       Created
#
# ==============================================================
# EXIT CODES:
#   0 - Normal exit
#   1 - General Error
# ==============================================================


#      ___       _ _   _       _ _
#     |_ _|_ __ (_) |_(_) __ _| (_)_______
#      | || '_ \| | __| |/ _` | | |_  / _ \
#      | || | | | | |_| | (_| | | |/ /  __/
#     |___|_| |_|_|\__|_|\__,_|_|_/___\___|
#

: "${SCRIPT_PATH:="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"}"
: "${SCRIPT_LOG_LIFETIME:=7}" # days
: "${SCRIPT_LOG_ID:=$$}"

SCRIPT_NAME="$( echo $(basename "$0") | cut -d '.' -f 1 )"
SCRIPT_LOG_PATH="${SCRIPT_PATH}/${SCRIPT_NAME}_log"
SCRIPT_TMP_PATH="${SCRIPT_PATH}/${SCRIPT_NAME}_tmp"
SCRIPT_LOG_FILE="$SCRIPT_LOG_PATH/${SCRIPT_NAME}_${SCRIPT_LOG_ID}_$(date '+%Y-%m-%d_%H-%M-%S_%N').log"

mkdir -p "$SCRIPT_LOG_PATH"
mkdir -p "$SCRIPT_TMP_PATH"
touch "$SCRIPT_LOG_FILE"


#      _____                 _   _
#     |  ___|   _ _ __   ___| |_(_) ___  _ __  ___
#     | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#     |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
#     |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#

print() 
{
    echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') |$SCRIPT_LEVEL_LABEL $@" | tee -a "$SCRIPT_LOG_FILE"
}

printi()
{
    SCRIPT_LEVEL_LABEL=" INFO:"
    print "$@"
    SCRIPT_LEVEL_LABEL=""
}

printw()
{
    SCRIPT_LEVEL_LABEL=" WARNING:"
    print "$@"
    SCRIPT_LEVEL_LABEL=""
}

printe()
{
    SCRIPT_LEVEL_LABEL=" ERROR:"
    print "$@"
    SCRIPT_LEVEL_LABEL=""
}

printfile () 
{
    while read line 
    do
        print ">> $line"
    done < "$1"
}

printl()
{
    print
    print "╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗"
    print "║                                                                                                        ║"

    logger_index=1
    while [ ! -z "$1" ]; do
        print "$(printf "║       %-25s : %-65s    ║" "$1" "$2")"
        shift 2
    done

    print "║                                                                                                        ║"
    print "╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝"
    print
}

printh ()
{
    print
    print "╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗"
    print "║                                                                                                        ║"
    while [ ! -z "$1" ]; do
        print "$(printf "║       %-93s    ║" "$1")"
        shift
    done
    print "║                                                                                                        ║"
    print "╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝"
    print
}

printhr ()
{
    print "----------------------------------------------------------------------------------------------------------"
}

printbox ()
{
    print "╔═$(echo -n "$@" | sed "s/./═/g")═╗"
    print "║ $@ ║" 
    print "╚═$(echo -n "$@" | sed "s/./═/g")═╝"
}

exit_ok ()
{
    printbox "Done."
    exit 0
}

exit_fail ()
{
    printhr
    printe "Failed - $2"
    printhr
    exit $1
}

create_tmp_file()
{
    tmp_file_full_path="$SCRIPT_TMP_PATH/${SCRIPT_NAME}_${SCRIPT_LOG_ID}_$1_$(date '+%Y-%m-%d_%H-%M-%S_%N').tmp.$2"
    touch "$tmp_file_full_path"
    echo  "$tmp_file_full_path"
}

clean_old_log ()
{
    find "$SCRIPT_LOG_PATH" -maxdepth 1 -type f -mtime +$SCRIPT_LOG_LIFETIME -name "*.log" -exec rm {} \;
}

clean_old_tmp ()
{
    find "$SCRIPT_LOG_PATH" -maxdepth 1 -type f -mtime +$SCRIPT_LOG_LIFETIME -name "*.tmp.*" -exec rm {} \;
}

change_log_id ()
{
    SCRIPT_LOG_ID="$@"
    SCRIPT_LOG_FILE_OLD="$SCRIPT_LOG_FILE"
    SCRIPT_LOG_FILE="$SCRIPT_LOG_PATH/${SCRIPT_NAME}_${SCRIPT_LOG_ID}_$(date '+%Y-%m-%d_%H-%M-%S_%N').log"
    mv "$SCRIPT_LOG_FILE_OLD" "$SCRIPT_LOG_FILE"
}

#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

# ===
# Include logger
# ===
. $SWD/logger.sh

clean_old_log
clean_old_tmp

printbox "Post Create Command"

# ===
# Install requirements and privpackages
# ===
cd "$SWD/../src"
printbox "Install requirements and privpackages"

# [ -f ../.env ] || exit_fail 64 ".env file not found."
# printi "Source .env file..."
# set -a
# . ../.env
# set +a

printi "pip install --upgrade pip"
pip install --upgrade pip

printi "touch requirements.txt"
touch requirements.txt

printi "touch privpackages.txt"
touch privpackages.txt

printi "pip install -r requirements.txt"
pip install -r requirements.txt || exit_fail 65 "Pip \`requirements.txt\` installation fails."

printi "pip install -r privpackages.txt"
pip install -r privpackages.txt || exit_fail 66 "Pip \`privpackages.txt\` installation fails"

exit_ok
#!/bin/bash

SWD="$( cd "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

cd "$SWD/../src"

pip freeze > requirements.txt
sed -i '/git\+/d' requirements.txt

echo Done.
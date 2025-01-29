#!/bin/bash

source .env
dataset_path=${PROJECT_PATH}gtfx_dataset/

if [ "$1" = "-clean" ] && [ -e ${dataset_path}data/ ]; then
    rm -r ${dataset_path}data/
fi
source ${dataset_path}src/.venv/bin/activate
(time python3 ${dataset_path}/src/main.py) > run.log 2>&1
deactivate

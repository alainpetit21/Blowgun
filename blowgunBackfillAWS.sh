#! /bin/bash

cd /home/ec2-user/Bianisoft/Code/Blowgun/
export PYTHONPATH=${PYTHONPATH}:${PWD}
source ./run_venv/bin/activate

COMMAND=blowgunBackfill
DONEYET="${COMMAND}.alreadyrun"

if [[ -f $DONEYET ]]; then
  exit 1
fi
touch "$DONEYET"

python ./src/mainBackfill.py

rm "$DONEYET"

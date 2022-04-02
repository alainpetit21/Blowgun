#! /bin/bash

cd /home/apetit/Work/Bianisoft/Code/Blowgun
export PYTHONPATH=${PYTHONPATH}:${PWD}
source ./venv/bin/activate

COMMAND=blowgunBackfill
DONEYET="${COMMAND}.alreadyrun"

if [[ -f $DONEYET ]]; then
  exit 1
fi
touch "$DONEYET"

python ./src/main.py

rm "$DONEYET"

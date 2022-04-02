#! /bin/bash

cd /home/ec2-user/Bianisoft/Code/Blowgun/
export PYTHONPATH=${PYTHONPATH}:${PWD}
source ./run_env/bin/activate

COMMAND=blowgun
DONEYET="${COMMAND}.alreadyrun"

if [[ -f $DONEYET ]]; then
  exit 1
fi
touch "$DONEYET"

python ./src/main.py

rm "$DONEYET"

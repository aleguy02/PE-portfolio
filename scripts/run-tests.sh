#bin/bash

set -eu

PROJECT_DIR=$PWD
echo $PROJECT_DIR
VENV_DIR="python3-virtualenv"


echo "=== setting up testing environment==="

source $VENV_DIR/bin/activate && pip install -r requirements.txt
export PYTHONPATH=":/"


echo "=== running unittest tests==="

$PROJECT_DIR/$VENV_DIR/bin/python -m unittest discover -v tests/


echo "=== running pytest tests==="

pytest
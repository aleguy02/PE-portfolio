#!/bin/bash
# Set up a virtual environment "python3-virtualenv" before executing this script

set -eo pipefail

PROJECT_DIR="$HOME/PE-portfolio/"
VENV_DIR="python3-virtualenv"
URL="http://alejandrovillate.duckdns.org:5000/"
SERVICE="myportfolio"


echo "=== pulling in latest changes ==="

cd $PROJECT_DIR
git fetch && git reset origin/main --hard
source $VENV_DIR/bin/activate && pip install -r requirements.txt


echo "=== restarting service ==="

systemctl daemon-reload
systemctl restart $SERVICE


echo "=== validating service ==="

if [ -z "$(systemctl status $SERVICE | grep "active (running)")" ]; then
        echo "!! service not running !!"
        exit 1
fi

if [ "$(curl --head $URL | awk '/^HTTP/{print $2}')" != "200" ]; then
        echo "Could not reach the site at $URL or received a non-200 HTTP response."
        exit 1
fi


echo "=== redeployment complete ==="

echo "View the site at $URL"
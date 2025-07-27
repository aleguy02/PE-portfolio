#!/bin/bash
# Set up a virtual environment "python3-virtualenv" before executing this script

set -eo pipefail

PROJECT_DIR="$HOME/PE-portfolio/"
VENV_DIR="python3-virtualenv"
URL="http://alejandrovillate.duckdns.org:5000/"
MAX_RETRIES=5


echo "=== pulling in latest changes ==="

cd $PROJECT_DIR
git fetch && git reset origin/main --hard > /dev/null
source $VENV_DIR/bin/activate && pip install -r requirements.txt > /dev/null


echo "=== spinning down containers ==="

docker compose -f compose.prod.yaml down > /dev/null


echo "=== rebuilding containers ==="

docker compose -f compose.prod.yaml up -d --build > /dev/null


echo "=== validating service ==="

expected_containers='myportfolio
running
mysql
running'

if [ "$(docker ps --format 'json' | jq -r '.Names,.State')" != "$expected_containers" ]; then
        echo "!! Unexpected container processes. !!"
        exit 1
fi

# Health check with retries
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
        if [ "$(curl --head $URL | awk '/^HTTP/{print $2}')" = "200" ]; then
                echo "Health check passed"
                break
        fi

        retry_count=$((retry_count + 1))
        echo "Health check attempt $retry_count/$MAX_RETRIES failed"

        if [ $retry_count -lt $MAX_RETRIES ]; then
                echo "Retrying in 2 seconds..."
                sleep 2
        fi
done
if [ $retry_count -eq $MAX_RETRIES ]; then
        echo "!! Could not reach the site at $URL or received a non-200 HTTP response. !!"
        exit 1
fi


echo "=== redeployment complete ==="

echo "View the site at $URL"
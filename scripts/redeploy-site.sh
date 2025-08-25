#!/bin/bash
# Set up a virtual environment "python3-virtualenv" before executing this script

set -eo pipefail

PROJECT_DIR="$HOME/PE-portfolio/"
VENV_DIR="python3-virtualenv"
URL="https://alejandrovillate.com"
MAX_RETRIES=5


echo "=== pulling in latest changes ==="

cd $PROJECT_DIR
git fetch && git reset origin/main --hard > /dev/null


echo "=== spinning down containers ==="

docker compose -f compose.prod.yaml down > /dev/null


echo "=== rebuilding containers ==="

docker compose -f compose.prod.yaml up -d --build > /dev/null


echo "=== validating service ==="

required_containers=("nginx" "myportfolio" "mysql")

for container in "${required_containers[@]}"; do
        if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
                echo "!! Required container '$container' is not running. !!"
                exit 1
        fi
done

# Health check with retries
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
        if [ "$(curl --head $URL/health | awk '/^HTTP/{print $2}')" = "200" ]; then
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
        echo "!! Could not reach the site at $URL/health or received a non-200 HTTP response. !!"
        exit 1
fi


echo "=== redeployment complete ==="

echo "View the site at $URL"

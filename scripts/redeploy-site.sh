#!/bin/bash

set -eo pipefail

echo "" > deploy.log
exec > >(tee -a deploy.log) 2>&1

PROJECT_DIR="$HOME/PE-portfolio/"
URL="https://www.alejandrovillate.com"
MAX_RETRIES=5



cd $PROJECT_DIR

printf "=== spinning down containers ==="
docker compose -f compose.prod.yaml down

printf "\n=== pulling in latest changes ==="
git fetch && git reset origin/main --hard

printf "\n=== rebuilding containers ==="
docker compose -f compose.prod.yaml up -d --build

printf "\n=== validating service ==="
required_containers=("myportfolio" "mysql")

for container in "${required_containers[@]}"; do
        if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
                echo "!! Required container '$container' is not running. !!"
                exit 1
        fi
done

# Health check with retries
# retry_count=0
# while [ $retry_count -lt $MAX_RETRIES ]; do
#         if [ "$(curl --head $URL/health | awk '/^HTTP/{print $2}')" = "200" ]; then
#                 echo "Health check passed"
#                 break
#         fi

#         retry_count=$((retry_count + 1))
#         echo "Health check attempt $retry_count/$MAX_RETRIES failed"

#         if [ $retry_count -lt $MAX_RETRIES ]; then
#                 echo "Retrying in 7 seconds..."
#                 sleep 7
#         fi
# done
# if [ $retry_count -eq $MAX_RETRIES ]; then
#         echo "!! Could not reach the site at $URL/health or received a non-200 HTTP response. !!"
#         exit 1
# fi


printf "\n=== redeployment complete ==="

echo "View the site at $URL"

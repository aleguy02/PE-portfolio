#!/bin/bash

# TODO: set up test environment instead of testing prod server to avoid race conditions

set -euo pipefail  # shoutout to Isaac from Splunk for this tip

BASE_URL="http://alejandrovillate.duckdns.org:5000"
API_URL="$BASE_URL/api/timeline_post"
POST_DATA="name=aname&email=e@mail.com&content=curl-test.sh"

echo "=== pinging $BASE_URL ==="
curl --head "$BASE_URL"
if [ $? -eq 7 ]; then
    echo "Could not reach $BASE_URL. Check that app is running"
    exit 1
fi

echo "=== making post request ==="
post=$(curl -s -X POST "$API_URL" -d "$POST_DATA" | jq -c '{content, email, id, name}')  # ignore `created_at` property to avoid race conditions
if [ -z "$post" ]; then
    echo "Error: Failed to create post."
    exit 1
fi

echo "=== making get request ==="
top=$(curl -s -X GET "$API_URL" | jq -c '.timeline_posts[0] | {content, email, id, name}')
if [ -z "$top" ]; then
    echo "Error: Failed to fetch posts."
    exit 1
fi

echo "=== comparing posts ==="
if [ "$post" != "$top" ]; then
    echo "Error: The created post does not match the most recent post."
    echo "Created: $post"
    echo "Fetched: $top"
    exit 1
fi

echo "=== success. cleaning up==="
curl -X DELETE "$API_URL"
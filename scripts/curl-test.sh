#!/bin/bash
#
# Written by : Alejandro Villate

set -euo pipefail  # shoutout to Isaac from Splunk for this tip

API_URL="http://localhost:5000/api/timeline_post"
POST_DATA="name=aname&email=e@mail.com&content=curl-test.sh"

post=$(curl -s -X POST "$API_URL" -d "$POST_DATA" | jq -c '{content, email, id, name}')  # ignore `created_at` property to avoid race conditions
if [ -z "$post" ]; then
    echo "Error: Failed to create post."
    exit 1
fi

# Fetch most recent post
top=$(curl -s -X GET "$API_URL" | jq -c '.timeline_posts[0] | {content, email, id, name}')
if [ -z "$top" ]; then
    echo "Error: Failed to fetch posts."
    exit 1
fi

if [ "$post" != "$top" ]; then
    echo "Error: The created post does not match the most recent post."
    echo "Created: $post"
    echo "Fetched: $top"
fi

# CLEAN UP
curl -s -X DELETE http://localhost:5000/api/timeline_post > /dev/null
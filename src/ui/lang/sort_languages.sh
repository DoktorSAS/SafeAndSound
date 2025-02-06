#!/bin/bash

# Path to the JSON file
JSON_FILE="./lang/languages.json"

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install jq to sort JSON files."
    exit 1
fi

# Sort the JSON using jq
jq 'sort_by(.id)' "$JSON_FILE" > temp.json && mv temp.json "$JSON_FILE"

echo "JSON file has been sorted alphabetically by 'id'."
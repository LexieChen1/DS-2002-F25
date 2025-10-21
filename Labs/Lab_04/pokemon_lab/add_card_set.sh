#!/bin/bash

# prompt user for the set ID
read -p "Enter the card set ID (base0, base2): " SET_ID
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

# tell user it's fetching 
echo "Fetching card data for set: $SET_ID ..."

# use curl to fetch data from api and validate JSON
response=$(curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID")

# check if response is valid JSON using jq
if echo "$response" | jq empty > /dev/null 2>&1; then
    echo "$response" | jq . > "card_set_lookup/${SET_ID}.json"
    echo "Saved to card_set_lookup/${SET_ID}.json"
else
    echo "Error: Invalid JSON response for $SET_ID — check network or API" >&2
    echo "$response" > "card_set_lookup/${SET_ID}_error.txt"
fi

#!/bin/bash

echo "Refreshing all cards in card_setup_lookup/ ..."

#loop through every .json file
for FILE in card_set_lookup/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Updating set: $SET_ID..."
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" | jq . > "$FILE"
    echo "Data written to $FILE"
done

echo "All card sets have been refreshed!"


    

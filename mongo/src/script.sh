#!/bin/bash

DB_NAME="aac"

mongoimport --db $DB_NAME \
            --collection animals \
            --mode upsert\
            --type csv \
            --headerline \
            --file /tmp/data.csv

mongoimport --db $DB_NAME \
            --collection rescue_profiles \
            --file /tmp/rescue_profiles.json \
            --jsonArray

echo "=== Import complete ==="
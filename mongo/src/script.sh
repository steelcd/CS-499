#!/bin/bash

DB_NAME="aac"
COLL_NAME="animals"
mongoimport --db $DB_NAME \
            --collection $COLL_NAME \
            --mode upsert\
            --type csv \
            --headerline \
            --file /tmp/data.csv

echo "=== Import complete ==="
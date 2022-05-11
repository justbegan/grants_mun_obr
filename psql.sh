#!/bin/sh

export $(cat .env | grep '^[[:blank:]]*[^[:blank:]#;]' | xargs)

PGPASSWORD=$POSTGRES_PASSWORD

docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB "$@"

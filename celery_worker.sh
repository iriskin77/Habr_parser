#!/bin/sh

until cd /parser
do
    echo "Waiting for server volume..."
done

celery -A parser worker -l -info

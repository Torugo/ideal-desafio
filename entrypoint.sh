#!/bin/bash

if [ ! -d "./migrations" ] 
then
    flask db init
    flask db migrate
    flask db upgrade
fi

python -m flask run --host=0.0.0.0 --port=5050
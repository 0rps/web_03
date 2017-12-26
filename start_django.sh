#!/bin/bash

cd ask
wsgi_app_name='ask.wsgi:application'
port='8000'

gunicorn -b "0.0.0.0:$port" -w 2 -t 15 "$wsgi_app_name" &
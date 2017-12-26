#!/bin/bash

wsgi_app_name='hello:app'
port='8080'

gunicorn -b "0.0.0.0:$port" -w 2 -t 15 "$wsgi_app_name" &
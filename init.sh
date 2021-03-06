#!/bin/bash

./create_db

cur_path=`pwd`
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-enabled/nginx.conf
sudo ln -s "$cur_path/etc/nginx.conf" /etc/nginx/sites-enabled/nginx.conf
sudo service nginx restart

sudo mkdir /etc/gunicorn.d
sudo rm /etc/gunicorn.d/hello.py
sudo ln -s "$cur_path/hello.py" /etc/gunicorn.d/hello.py

./start_hello.sh
./start_django.sh

# cd /etc/gunicorn.d
# gunicorn -b 0.0.0.0:8080 hello:app &

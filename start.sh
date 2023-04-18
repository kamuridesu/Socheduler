#! /usr/bin/bash
set -a
source ./.env
set +a
cd Socheduler
python manage.py runserver 0.0.0.0:8000

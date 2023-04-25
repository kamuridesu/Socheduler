#! /usr/bin/bash
set -a
source ./.env
set +a
cd Socheduler
python manage.py makemigrations frontend && python manage.py migrate frontend --noinput
python manage.py makemigrations && python manage.py migrate --noinput
if [[ ! -f "./done.confirm" ]]; then
    python manage.py createsuperuser --noinput --username kamuri --email "micaelmorim@gmail.com"
    python manage.py shell -c 'import os; from allauth.socialaccount.models import SocialApp; all_sa = SocialApp.objects.all(); SocialApp.objects.create(provider="github",client_id=os.getenv("GITHUB_CLIENT_ID"),secret=os.getenv("GITHUB_CLIENT_SECRET"),name="Github") if len(all_sa) == 0 else print("Social App already exists")'
    echo "done" > done.confirm
fi
python manage.py runserver 0.0.0.0:8000

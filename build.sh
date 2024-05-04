#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py makemigrations sbook
python manage.py makemigrations note
python manage.py makemigrations chatty
python manage.py migrate sbook
python manage.py migrate note
python manage.py migrate chatty

#python manage.py createsuperuser --username ken-morel --password amemimy114865009

echo all zell

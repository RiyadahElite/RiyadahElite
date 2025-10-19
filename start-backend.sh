#!/bin/bash

cd "$(dirname "$0")"

echo "Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

echo "Running Django migrations..."
python3 manage.py migrate

echo "Starting Django development server on http://127.0.0.1:8000..."
python3 manage.py runserver 127.0.0.1:8000

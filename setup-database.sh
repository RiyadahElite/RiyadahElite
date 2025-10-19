#!/bin/bash

echo "Setting up Riyadh Elite Database..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python dependencies"
    exit 1
fi

echo "Creating database migrations..."
python3 manage.py makemigrations

if [ $? -ne 0 ]; then
    echo "Error: Failed to create migrations"
    exit 1
fi

echo "Applying migrations..."
python3 manage.py migrate

if [ $? -ne 0 ]; then
    echo "Error: Failed to apply migrations"
    exit 1
fi

echo "Creating superuser (admin)..."
echo "You will be prompted to create an admin account"
python3 manage.py createsuperuser

echo ""
echo "Database setup complete!"
echo "You can now start the backend server with: ./start-backend.sh"
echo "Access Django admin at: http://127.0.0.1:8000/admin"

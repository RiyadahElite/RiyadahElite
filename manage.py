#!/usr/bin/env python
"""Django's command-line utility for administrative tasks, with embedded environment variables."""

import os
import sys

# ==========================
# Set environment variables here (replace values with your own)
# ==========================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Example environment variables from .env
# You can add more here as needed for your project
os.environ.setdefault('SECRET_KEY', 'your-secret-key-here')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('DB_ENGINE', 'django.db.backends.postgresql')
os.environ.setdefault('DB_NAME', 'your_db_name')
os.environ.setdefault('DB_USER', 'your_db_user')
os.environ.setdefault('DB_PASSWORD', 'your_db_password')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
# Add any other environment variables you need for your backend

def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

#!/bin/bash

# Enhanced setup script for Cynthia Online Store on Ubuntu/Linux
# Handles database setup, migrations, and demo data

set -e  # Exit on any error

echo "========================================"
echo "Cynthia Online Store - Ubuntu/Linux Setup"
echo "Contact: cynthy8samuels@gmail.com"
echo "Phone: +254798534856"
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Check if venv module is available
if ! python3 -c "import venv" &> /dev/null; then
    echo "python3-venv is not installed. Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Run deployment setup
echo "Running deployment setup..."
python scripts/deploy_setup.py

# Ask user if they want to setup demo data
read -p "Do you want to setup demo data? (y/n): " setup_demo
if [[ $setup_demo =~ ^[Yy]$ ]]; then
    echo "Setting up demo data..."
    python scripts/setup_demo_data.py
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Access the admin panel at:"
echo "  http://localhost:8000/admin/"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "API Documentation:"
echo "  http://localhost:8000/swagger/"
echo "========================================"

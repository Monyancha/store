@echo off
REM Enhanced setup script for Cynthia Online Store on Windows
REM Handles database setup, migrations, and demo data

echo ========================================
echo Cynthia Online Store - Windows Setup
echo Contact: cynthy8samuels@gmail.com
echo Phone: +254798534856
echo ========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

REM Run migrations
echo Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo Failed to run migrations.
    pause
    exit /b 1
)

REM Create superuser if needed
echo Checking for superuser...
python scripts\deploy_setup.py

REM Ask user if they want to setup demo data
set /p setup_demo="Do you want to setup demo data? (y/n): "
if /i "%setup_demo%"=="y" (
    echo Setting up demo data...
    python scripts\setup_demo_data.py
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Setup completed successfully!
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Access the admin panel at:
echo   http://localhost:8000/admin/
echo   Username: admin
echo   Password: admin
echo.
echo API Documentation:
echo   http://localhost:8000/swagger/
echo ========================================
pause

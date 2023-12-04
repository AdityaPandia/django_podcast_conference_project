# Droid Kaigi Backend

Staging: https://droidkaigi.pythonanywhere.com

## Getting started
### Requirements
 - Python 3.11
 - PIP
 - venv

### Installation
```bash
# Clone the repository
git clone https://github.com/omganeshdahale/droid-kaigi-backend.git

# Enter into the directory
cd droid-kaigi-backend/

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Load data
python manage.py loaddata datadump.json
```

### Starting the application
```bash
python manage.py runserver
```

## Production
Follow this guide for deployment: <br>
https://github.com/mitchtabian/HOWTO-django-channels-daphne
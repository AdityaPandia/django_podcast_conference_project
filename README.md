# Droid Kaigi Backend

Reference: https://github.com/mitchtabian/HOWTO-django-channels-daphne

### Install Server Dependencies
```bash
passwd
sudo apt update
sudo apt install python3.11 python3-pip python3.11-dev python3.11-venv libpq-dev postgresql postgresql-contrib nginx curl git-all
sudo apt install libgl1-mesa-glx # Resolve cv2 issue
```

### Setup Database
```bash
sudo -u postgres psql
CREATE DATABASE django_db;
CREATE USER django WITH PASSWORD 'password';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_db TO django;
\q
```

### Install Project
```bash
# User and Basic directory structure
adduser django
su django
cd /home/django/
mkdir CodingWithMitchChat
cd CodingWithMitchChat
python3.11 -m venv venv
source venv/bin/activate
mkdir src
cd src

# Pull the repository
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub  # Copy the output and create deployment key
git init
git remote add origin https://github.com/omganeshdahale/droid-kaigi-backend.git
git pull origin prod

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata datadump.json
python manage.py collectstatic
```

### Check if you can run your project
```bash
python manage.py runserver 0.0.0.0:8000
# visit http://<your_ip_address>:8000/

gunicorn --bind 0.0.0.0:8000 myproject.wsgi
# visit http://<your_ip_address>:8000/
```

### Creating systemd Socket and Service Files for Gunicorn
```bash
su root
cd /etc/systemd/system/
```
Do `nano gunicorn.socket` and paste the following
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
`ctrl+x` then `Y` then `enter` to save

Do `nano gunicorn.service` and paste the following
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/CodingWithMitchChat/src
ExecStart=/home/django/CodingWithMitchChat/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
`ctrl+x` then `Y` then `enter` to save

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

#### Helpful Commands
1. `sudo systemctl daemon-reload`
    - Must be executed if you change the `gunicorn.service` file.
1. `sudo systemctl restart gunicorn`
    - If you change code on your server you must execute this to see the changes take place.
1. `sudo systemctl status gunicorn`
1. `sudo shutdown -r now`
    - restart the server

### Configure Nginx to Proxy Pass to Gunicorn
```bash
cd /etc/nginx/sites-available
```
Do `nano CodingWithMitchChat` and paste the following
```nginx
server {
    server_name <your_ip_address>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/django/CodingWithMitchChat/src;
    }
    
     location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
    

}
```
`ctrl+x` then `Y` then `enter` to save

Do `nano /etc/nginx/nginx.conf` and update the following 
so we can upload large files (images)
```nginx
http{
	...
	client_max_body_size 10M; 
}
```
`ctrl+x` then `Y` then `enter` to save

#### Configure firewall
```bash
sudo ln -s /etc/nginx/sites-available/CodingWithMitchChat /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
sudo systemctl restart gunicorn
sudo shutdown -r now
```
Visit http://<your_ip_address>/

### DEBUGGING
Here are some commands you can use to look at the server logs. **These commands are absolutely crucial to know.** If your server randomly isn't working one day, this is what you use to start debugging.
1. `sudo journalctl` is where all the logs are consolidated to. That's usually where I check.
1. `sudo tail -F /var/log/nginx/error.log` View the last entries in the error log
1. `sudo journalctl -u nginx` Nginx process logs 
1. `sudo less /var/log/nginx/access.log` Nginx access logs
1. `sudo less /var/log/nginx/error.log` Nginx error logs
1. `sudo journalctl -u gunicorn` gunicorn application logs
1. `sudo journalctl -u gunicorn.socket` check gunicorn socket logs
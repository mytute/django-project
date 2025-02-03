# Deploying your application 

first you need to create new droplet in Digital Ocean service.  

to login to droplet open cmd and enter following commands   
```bash 
$ ssh root@ip_address_of_your_droplet  
```

to install software updates on vm  
```bash 
$ apt-get update && apt-get upgrade
```

set the host name for new vm   
```bash 
$ hostnamectl set-hostname django-server  
$ hostname # for test above cmd is worked or not.  

```

set hostname into host file.  
```bash 
$ vi /etc/hosts
# add following line to "host" file  
# 128.199.175.149 django-server

```

root user have unlimited access and to limited it we need to create another user that use admin cmd with "sudo" cmd.  
```bash 
$ adduser swasthi  
# just enough to add password and name of the user.

# add created user to "sudo" group  
$ adduser swasthi sudo 

# exit and login as new user  
$ exit
$ ssh swasthi@ip_address_of_your_droplet
```

setup ssh key to connect to the server.  
```bash 
# in remote machine  
# create ssh directory in vm if not there.  
# "-p" for No Error if Directory Already Exists and create parent directoris if the don't  
$ mkdir -p ~/.ssh

# in local machine  
$ ssh-keygen -b 4096 -t rsa -C "samadhivkcom@gmail.com" 
$ scp ~/.ssh/id_rsa.pub swasthi@ip_address_of_your_droplet:~/.ssh/authorized_keys  

# in remove machine  
# check is file copied  
$ ls .ssh  
# set .ssh directory read/write/execute permissions  
$ sudo chmod 700 ~/.ssh  
# set .ssh files read/write permissions  
$ sudo chmod 600 ~/.ssh/*  

# in local machine now you can login without password  
$ ssh root@ip_address_of_your_droplet  

```

in the remove server privent root login and password authentication.  
```bash 
# go to config file
$ sudo vi /etc/ssh/sshd_config

# update following properties in the "sshd_config" file  
PermitRootLogin no
PasswordAuthentication no  

# restart the ssh service (ssd or sshd)  
$ sudo systemctl restart ssh

# still if you can log with password then you change check override config inside "ssh" folder.   
# after found you have update it.  
# sudo sshd -T | grep passwordauthentication # check config has change or not 
# sudo grep -r "PasswordAuthentication" /etc/ssh/sshd_config.d/
$ ssh -o PreferredAuthentications=password root@152.42.219.79
```

let's configur the firewall 
```bash 
# install uncomplicated firewall   
$ sudo apt-get install ufw  

# block outgoing   
$ sudo ufw default allow outgoing  

# block all incoming  
$ sudo ufw default deny incoming  

$ sudo ufw allow ssh  
$ sudo ufw allow 8000  
$ sudo ufw enable 
# check list of status  
$ sudo ufw status
$ sudo ufw status verbose # get more details
```

virtualenv is the way to separate different Python environment  
```bash

# install and check the virtualenv package  
$ pip install virtualenv  
$ virtualenv --version

# navigate to your Django project 
# create new virtual environment  
$ virtualenv venv  
# activate new virtual environment  
$ source venv/bin/activate  
# deactivate activated virtual environment  
$ deactivate  
# check install packages to the virtual environment  
$ pip list  
$ pip freeze  

# copy used dependencies to "requirements.txt" file.(location where has manage.py file in the project)   
$ pip freeze > requirements.txt  
```

let pull django project from local machine to the remote server  
```bash
$ scp -r django_project swasthi@157.230.242.49:~/
```

next you have to install dependecies to your remote server.  
```
$ sudo apt-get install python3-pip  
$ sudo apt-get install python3-venv  
# create new virtual env in remote server name "venv" (location where mange.py file)
$ python -m venv django_project/django_project/venv  
# activate "venv" virtual environment in server  
$ source venv/bin/activate  

# install packages in "requirements.txt" file. 
$ pip install -r requirements.txt  
```

let's change some setting of django project for run on server for test 
```bash 
# open settings.py file for add domain ip address to ALLOWED_HOSTS array.    
ALLOWED_HOSTS = ['157.230.242.49']

# change static url in the settings.py file  
STATIC_ROOT =  os.path.join(BASE_DIR, 'static') # add here  

# run following command for copy static files to new directory     
$ python manage.py collectstatic
# after above command you can see "static" folder where "manage.py" file have. 

# run server  
$ python manage.py runserver 0.0.0.0:8000
```

run django application with apache2  
```bash 
# install apache server   
$ sudo apt-get install apache2  

# install wsgi for comminication server with django application   
$ sudo apt-get install libapache2-mod-wsgi-py3

# configure apache web server  
$ cd /etc/apache2/sites-available 

# copy default file for create config  
$ sudo cp 000-default.conf django_project.conf 

# inside "VirtualHost" put following rules   
<VirtualHost:80>

    Alias /static /home/swasthi/django_project/static 
    <Directory /home/swasthi/django_project/static>
      Require all granted
    </Directory>
    Alias /media /home/swasthi/django_project/media 
    <Directory /home/swasthi/django_project/media>
      Require all granted
    </Directory>

    <Directory /home/swasthi/django_project/django_project>
      <Files wsgi.py>
        Require all granted
      </Files>
    </Directory>

    WSGIScriptAlias / /home/swasthi/django_project/django_project/wsgi.py  
    WSGIDaemonProcess django_app python-path=/home/swasthi/django_project python-home=/home/swasthi/django_project/venv
    WSGIProcessGroup django_app   

</VirtualHost>

# let enable site throgh apache(activate) 
$ sudo a2ensite django_project  

# to disable default apache configurations  
$ sudo a2dissite 000-default.conf  

# set file permissions  
# give apache to access sqlite3 files (this for when only use sqlite)
$ sudo chown :www-data django_project/db.sqlite3  
$ sudo chmod 664 django_project/db.sqlite3   
$ sudo chown :www-data django_project/  

# for media file 
$ sudo chown -R :www-data django_project/media/  
$ sudo chmod -R 775 django_project/media
```

setup env variables inside server chmod 
create config.json file inside "etc" folder.  
```bash
$ vi /etc/config.json  
```

> /etc/config.json  (in remote server)  
```json 
{
    "SECRET_KEY": "django-insecure-+^9n#xfmzyq8)jodreh6g399vmy(vot%h)i)+e3zc5_7mr+8rz",
    "EMAIL_USER": "devmius@gmail.com",
    "EMAIL_PASS": "nizo trsf bwgx mspo",
}
```

update "settings.py" file to get above values from "config.json" file.  
> django_project/django_project/settings.py 
```py 
import json  
with open('/etc/config.json') as config_file:
  config = json.load(config_file)

SECRET_KEY = config['SECRET_KEY']
DEBUG = False  

EMAIL_HOST_USER = config.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL_PASS')
```

after setup apache server we can deny port 8000 and add http/tcp port for ufw  
```bash 
$ sudo ufw delete allow 8000 
$ sudo ufw allow http/tcp 
# for restart apache server  
$ sudo service apache2 restart  
```

if you using some database other than sqlite then install following python packages  
```bash
$ sudo apt install python3-dev
$ pip install psycopg2-binary # in virtual environment
```

Create a Gunicorn Systemd Service in "gunicorn.service"  
```bash 
$ sudo vi /etc/systemd/system/gunicorn.service
```
>/etc/systemd/system/gunicorn.service
```bash 
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=swasthi
Group=www-data
WorkingDirectory=/home/swasthi/django_project
ExecStart=/home/swasthi/django_project/venv/bin/gunicorn --workers 3 --bind unix:/home/swasthi/django_project/gunicorn.sock django_project.wsgi:application

[Install]
WantedBy=multi-user.target
```
start and enable Gunicorn  
```bash 
$ sudo systemctl start gunicorn
$ sudo systemctl enable gunicorn
$ sudo systemctl status gunicorn
```

Configure Nginx 
```bash 
$ sudo vi /etc/nginx/sites-available/django_project # django_project is file name as your desire.  
```
> /etc/nginx/sites-available/django_project
```bash 
server {
    listen 80;
    server_name 192.168.1.100;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/swasthi/django_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/swasthi/django_project/gunicorn.sock;
    }
}
```
enable the nginx configurations   
```bash 
$ sudo ln -s /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/
$ sudo nginx -t
$ sudo systemctl restart nginx
```
Allow traffic on port 80:  
```
$ sudo ufw allow 'Nginx Full'
$ sudo ufw enable
```

Restart Services  
```bash 
$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```

set permissions for nginx and gunicorn 
```bash 
$ sudo chmod 664 /home/swasthi/django_project/gunicorn.sock
$ sudo chown swasthi:www-data /home/swasthi/django_project/gunicorn.sock

$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```
to resolve permission issue permanently  
```bash 
$ sudo usermod -aG swasthi www-data
$ sudo reboot
```

Secure Your Subdomain with HTTPS (SSL)  
```bash 
$ sudo apt install certbot python3-certbot-nginx -y
$ sudo certbot --nginx -d app.example.com

# for automatic renewal  
$ sudo systemctl enable certbot.timer
$ sudo certbot renew --dry-run
```

## add MySql instead of SQlite  
install "mysql-server" and "mysql-client"  
```bash 
$ sudo apt update
$ sudo apt install mysql-server mysql-client -y

# after installation, secure your MySql
$ sudo mysql_secure_installation
```

Install MySQL Python Connector  
```bash 
$ sudo apt install libmysqlclient-dev
# after set virtual environment  
$ pip install mysqlclient
# if there error while installing "mysqlclient"  
$ sudo apt install python3-dev default-libmysqlclient-dev build-essential


# if there error while installing "mysqlclient" then install "pymysql" package  
$ pip install pymysql

if you need to hash password then install following package  
$ pip install cryptography
```

if you install "pymysql" package then you need to change setting.py file   
```py 
import pymysql
pymysql.install_as_MySQLdb()
```

create database and user   
```bash 
# login to mysql without password when have sudo  
$ sudo mysql -u root -p

> CREATE DATABASE django_db;
> CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'yourpassword';
> GRANT ALL PRIVILEGES ON django_db.* TO 'django_user'@'localhost';
> FLUSH PRIVILEGES;
> EXIT;
```
Update settings.py to Use MySQL  
```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',  # Change if using a remote MySQL server
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

Apply Migrations  
```bash 
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ sudo systemctl restart mysql
```
If you're using Django's admin panel, create a superuser again:  
```bash 
$ python3 manage.py createsuperuser
```

Restart Gunicorn & Nginx 
```bash 
$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```

```bash 
$ pip install python-dotenv  
```

create .env file where "manage.py" file  
> django_project/.env  
```bash 
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=abcd@gmail.com
EMAIL_HOST_PASSWORD=1234 rty 678 qwe
```

Update "settings.py" file to load environment variables.  
```py 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Convert to integer
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1')  # Convert to boolean
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

restart your server   
```bash 
$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```
add ".env" file to ".gitignore" file  
```bash 
.env
```


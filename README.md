# Django Quick Practice On LOCAL 

```bash 
$ mkdir django-mysql && cd django-mysql
$ pip install virtualenv
$ virtualenv --version
$ virtualenv venv
$ source venv/bin/activate
$ pip list  
```

install the Python 3 and MySQL development headers and librarie    
[doc](https://pypi.org/project/mysqlclient/)  
```bash
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config # Debian / Ubuntu
$ sudo yum install python3-devel mysql-devel pkgconfig # Red Hat / CentOS
```

install django and mysql client for virtual env   
```bash
$ pip install django mysqlclient
$ pip install gunicorn # For production deployment
$ pip install mysqlclient # driver for MySQL (use psycopg2-binary==2.9.9 for PostgreSQL)
```

Create the Django project and app
```bash
$ django-admin startproject myproject .
$ cd myproject
$ python manage.py startapp myapp
```

### Configure MySQL Database  
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'root',
        'PASSWORD': 'rootpassword',
        'HOST': 'db',  # Docker container name
        'PORT': '3306',
    }
}
```

add newly created "myapp" app.py name to main settings.py file   
```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyappConfig' # add here  
]
```

run migrations    
```bash
$ python manage.py makemigrations myapp
$ python manage.py migrate
```

Create an admin interface in myapp/admin.py   
```bash 
from django.contrib import admin
from .models import Item

admin.site.register(Item)
```

install docker
```bash
$ sudo dnf install docker -y # for fedora
$ sudo apt install docker.io
```

generete requirements.txt file inside where have manage.py file.    
```bash
$ pip freeze > requirements.txt
```

install package for set dot env variables and create dot env file     
```bash
$ pip install python-dotenv
```
.env.local
```py
SECRET_KEY=local-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=mydatabase_local
DATABASE_USER=root
DATABASE_PASSWORD=root123
DATABASE_HOST=localhost
DATABASE_PORT=3306
```
.env.test
```py
SECRET_KEY=test-secret-key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=mydatabase_test
DATABASE_USER=test_user
DATABASE_PASSWORD=test_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

.env.prod
```py
SECRET_KEY=prod-secret-key
DEBUG=False
ALLOWED_HOSTS=mydomain.com,www.mydomain.com
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=mydatabase_prod
DATABASE_USER=prod_user
DATABASE_PASSWORD=prod_password
DATABASE_HOST=db.myserver.com
DATABASE_PORT=3306
```

add above dot env value to "settings.py" file   
```py
import os
from pathlib import Path
from dotenv import load_dotenv

# Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine the environment (default to local)
ENV = os.getenv("DJANGO_ENV", "local")

# Load the corresponding .env file
dotenv_file = f".env.{ENV}"
load_dotenv(os.path.join(BASE_DIR, dotenv_file))

# SECURITY SETTINGS
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

# STATIC FILES
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

Set the Environment Variable Before Running Django
For Local Development
```bash
$ export DJANGO_ENV=local
$ python manage.py runserver
```  
For Testing
```bash
export DJANGO_ENV=test
python manage.py test
```
For Production
```bash
export DJANGO_ENV=prod
gunicorn mydjango.wsgi
```

run application   
```bash
$ gunicorn myfjango.wsgi:application -b 0.0.0.0:8000
$ python manage.py runserver  # this method not sutable for production 
```

docker file  on root directory   
```bash
# Use an official Python runtime as a parent image
FROM python:3.10

# Set an environment variable to onbuffer Python output, aiding in loggin and debugging  
ENV PORT=8000 

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Upgrade pip to ensure we have the latest version for installing dependencies  
RUN pip install --upgrade pip  

# Install dependencies from the requirements.txt file to ensure our Python environment  
RUN pip install --no-cache-dir -r requirements.txt

# Run database migrations and start the server
# CMD gunicorn mydjango.wsgi:application --bind 0.0.0.0:"${PORT}"
CMD ["gunicorn", "mydjango.wsgi:application", "--bind", "0.0.0.0:8000"]

# Inform Docker that the container listens on the specified network port at runtime 
EXPOSE 8000
```

build docker  
```bash
$ sudo docker build -t mydjango-app .
$ sudo docker run -d -p 8000:8000 --name mydjango-container mydjango-app
```

### conflict between localhost of local machine and docker container.    

if your mysql not connecting with docker application it may conflict of locahost hot in local machine and docker container  
get ip address 
```bash
$ ip addr show docker0 # IP address of the docker0 network interface, which is the default virtual bridge network created by Docker on your host machine.
$ ip route | grep default | awk '{print $3}'  # extracts the default gateway IP 
```
put docker0 ip address for mysql host in django dot env file.   
```bash
SECRET_KEY=test-secret-ley
DEBUG=True
ALLOWED_HOSTS=localhost 
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=mydatabase
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=172.17.0.1 # add op address from docker0 (not localhost)
DATABASE_PORT=3306
```
```bash
$ mysql
> CREATE USER 'root'@'172.17.0.%' IDENTIFIED BY 'yourpassword';
> GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.17.0.%' WITH GRANT OPTION;
> FLUSH PRIVILEGES;
```
By default, MySQL only accepts connections from localhost (127.0.0.1) so need chage to all
```bash
$ sudo vi  /etc/my.cnf
# add following line to my.cnf file instead of bind-address = 127.0.0.1
# bind-address = 0.0.0.0 
```
restart mysql server from local machine  
```bash
$ sudo systemctl restart mysqld
```

### connect with mysql docker container    
```bash
$ docker pull mysql:latest # Pull the MySQL Docker Image

$ docker run -d --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=mydatabase \
  -e MYSQL_USER=myuser \
  -e MYSQL_PASSWORD=mypassword \
  -p 3307:3306 \
  -v mysql_data:/var/lib/mysql \
  --restart unless-stopped \
  mysql:latestm

$ sudo docker exec -it mysql-container mysql -u root -p

> mysql> create database mydatabase;

# use following url to login docker mysql for dbever
jdbc:mysql://localhost:3307/mydatabase?allowPublicKeyRetrieval=true&useSSL=false

# throught mysql-container make migrations 
$ sudo docker exec -it 11e29c840a9d bash
root@11e29c840a9d:/app# python manage.py migrate
```










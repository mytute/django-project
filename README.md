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


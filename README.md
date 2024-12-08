# Getting Started

install Django  
```bash ;
$ pip install django  
$ python -m django --version  
```

to see all the django shell commands  
```bash 
$ django-admin
```

to create new django project ('-' in the name not allowed)   
this will create folder with project name.  
```bash 
$ django-admin startproject django_project_name  
```

let's see about django project directory  
django_project # project name file    
  __init__.py  # python package   
  settings.py  # change settings and configurations  
  urls.py      # mapping urls  
  wsgi.py      # python web application and web server communicate(not touching this file)   
manage.py # allows us to run command line commands  

to run Django web application   
see on localhost:8000
```bash 
$ cd django_project_name
$ python manage.py runserver  
```




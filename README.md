# Admin Page      


to create superuser  
```bash 
$ python manage.py createsuperuser # getting error of no such a table   
```

to init database create following cmd   
```bash 
$ python manage.py makemigrations # for add new changes      
$ python manage.py migrate # apply migrations  
```

after init tables run createsuperuser cmd and input Username and Password.    
```bash 
$ python manage.py createsuperuser
```

now navigate admin page "localhost:8000/admin" and login.  

click add user button to create new user and add username password and save.   

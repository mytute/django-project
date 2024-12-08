# Applications and Routes  

in Django single project can contain multiple apps.    

let's create blog app in our project   
```bash  
$ python manage.py startapp app_name
$ python manage.py startapp blog  
```

see the newly created file under 'blog' folder   
blog   
  __init__.py     
  admin.py   
  apps.py  
  migrations  
    __init__.py  
  models.py  
  tests.py  
  views.py  
db.sqlite3  
django_project  
  __init__.py  
  settings.py  
  urls.py  
  wsgi.py  

>django_project/blog/views.py  
```py
from django.shortcuts import render
from django.http import HttpResponse # add 

# add view call home that map with "views.home"
def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

# add view call home that map with "views.about"
def about(request):
    return HttpResponse('<h1>Blog About</h1>')
```

create new file call "urls.py" inside "blog" app folder for map route of "blog" app.   
>django_project/blog/urls.py # this is urls module for blog app    
```py 
from django.urls import path 
from . import views  


urlpatterns = [
  path('', views.home, name='blog-home'),
  path('about/', views.about, name='blog-about')
]
```

import above "urls.py" module file into main "urls.py" file.  
>django_project/django_project/urls.py     
```py 
from django.contrib import admin
from django.urls import path, include # include add here.  

urlpatterns = [
    path('admin/', admin.site.urls),
    # include mehod check blog/urls.py file for any match of path urls that user entered  
    path('blog/', include('blog.urls')), # add here   
]
```

Django normally redirect route without forward slash so it good to add forward slash 'url_name/' end of the url name.    

If we want to blog as our home page of the website (localhost:8000)  we can make main 'urls.py' file "blog/" path empty.  
```py 
[

    path('', include('blog.urls')), # 'blog/' > ''   
]
```

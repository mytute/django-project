# Templetes    

if we return html file from 'views.py' file as "HttpResponse" the we have to repeate lot of html code. As a solution we can use "Templetes"  

create new folder call "templetes" inside "blog" folder. As Django naming convention we inside "templates" folder we need to create new folder with name app name here "blog"  

> django_project/blog/templates/blog/home.html   
```html 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
    <link href="css/style.css" rel="stylesheet">
  </head>
  <body>
    <h1>Blog home!</h1> 
  </body>
</html>
```

we have to add our "blog" application to our list of installed apps.   
each application has "app.py" file that have it's class that app config name.    

> django_project/blog/app.py  
```py 
from django.apps import AppConfig

class BlogConfig(AppConfig): # BlogConfig is blog app condig name that we need to add main "settings.py" list.  
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

> django_project/django_project/settings.py  
```py 
INSTALLED_APPS = [
    'blog.apps.BlogConfig', # add here
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

now there are several method to load a template. But good way to use is with django "shortcuts"   
> django_project/blog/views.py  
```py 
from django.shortcuts import render # import shortcuts method  
from django.http import HttpResponse

def home(request):
    #return HttpResponse('<h1>Blog Home</h1>') # basic way to return http response   
    return render(request, 'blog/home.html') # return http with template  

def about(request):
    return HttpResponse('<h1>Blog About</h1>')
```

show how to send data and manipulate them in "views.py" file.  
> django_project/blog/views.py  
```py 
from django.shortcuts import render
from django.http import HttpResponse

posts = [
        {
            'author': 'CoreyMS',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'August 27, 2018'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'August 28, 2018'
        }
        ]

def home(request):
    context = {
            'posts':posts
            }
    return render(request, 'blog/home.html', context) # pass data as third parameter   
```

show how to do manipulate passed data in html template file.  
show how to write "forloops" and "if/else" with ginger2 when receive data from "views.py" file to the template.   
```html 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!--how to write if/else conditions-->
    {% if title %}
      <title>{{title}}</title>
    {% else %}
      <title>default title</title>
    {% endif %}

    <link href="css/style.css" rel="stylesheet">
  </head>
  <body>
    <!--how to write for loops -->
    {% for post in posts %}
      <h1>{{ post.title }}</h1>
      <p>By {{ post.author }} on {{ post.date_posted }}</p>
      <p>{{ post.content }}</p>
    {% endfor %}
  </body>
</html>
```

show how to use template inheritance for reuse common template html code.   
create new template in our "templates/blog" folder call "base.html"  
block is a section that child section can override  

show how to store common html in to "base.html" file make "block content" where child code will replace.  
and add bootstrap to "base.html" file.   
```html 
<!DOCTYPE html>
<html lang="en">
  <head>
    <!--add bootstrap here-->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <!--how to write if/else conditions-->
    {% if title %}
      <title>{{title}}</title>
    {% else %}
      <title>default title</title>
    {% endif %}

    <link href="css/style.css" rel="stylesheet">
  </head>
  <body>
    <!--create block here for override from child templates -->
    {% block content %} {% endblock %}

     <!--add bootstrap here-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
  </body>
</html>
```

show how to update "home.html" file for inherite html code from "base.html" file.  
```html 
<!--first we need to import base.html file -->
{% extends "blog/base.html" %}
{% block content %}

    {% for post in posts %}
      <h1>{{ post.title }}</h1>
      <p>By {{ post.author }} on {{ post.date_posted }}</p>
      <p>{{ post.content }}</p>
    {% endfor %}

{% endblock content %}
```

for make css better    
go to "base.html" file and add following code at the start of body element   
```html 
<header class="site-header">
  <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
    <div class="container">
      <a class="navbar-brand mr-4" href="/">Django Blog</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarToggle">
        <div class="navbar-nav mr-auto">
          <a class="nav-item nav-link" href="/">Home</a>
          <a class="nav-item nav-link" href="/about">About</a>
        </div>
        <!-- Navbar Right Side -->
        <div class="navbar-nav">
          <a class="nav-item nav-link" href="#">Login</a>
          <a class="nav-item nav-link" href="#">Register</a>
        </div>
      </div>
    </div>
  </nav>
</header>
```
and in same page instead of "block content" copy and past following code  
```html 
<main role="main" class="container">
  <div class="row">
    <div class="col-md-8">
      {% block content %}{% endblock %}
    </div>
    <div class="col-md-4">
      <div class="content-section">
        <h3>Our Sidebar</h3>
        <p class='text-muted'>You can put any information here you'd like.
          <ul class="list-group">
            <li class="list-group-item list-group-item-light">Latest Posts</li>
            <li class="list-group-item list-group-item-light">Announcements</li>
            <li class="list-group-item list-group-item-light">Calendars</li>
            <li class="list-group-item list-group-item-light">etc</li>
          </ul>
        </p>
      </div>
    </div>
  </div>
</main>
```

show how to store our custom css file in the project.  
create a following naming convention folder structure to store css file and link with "base.html" file.   
> django_project/blog/static/blog/main.css  
```css 
body {
  background: #fafafa;
  color: #333333;
  margin-top: 5rem;
}

h1, h2, h3, h4, h5, h6 {
  color: #444444;
}

ul {
  margin: 0;
}

.bg-steel {
  background-color: #5f788a;
}

.site-header .navbar-nav .nav-link {
  color: #cbd5db;
}

.site-header .navbar-nav .nav-link:hover {
  color: #ffffff;
}

.site-header .navbar-nav .nav-link.active {
  font-weight: 500;
}

.content-section {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-bottom: 20px;
}

.article-title {
  color: #444444;
}

a.article-title:hover {
  color: #428bca;
  text-decoration: none;
}

.article-content {
  white-space: pre-line;
}

.article-img {
  height: 65px;
  width: 65px;
  margin-right: 16px;
}

.article-metadata {
  padding-bottom: 1px;
  margin-bottom: 4px;
  border-bottom: 1px solid #e3e3e3
}

.article-metadata a:hover {
  color: #333;
  text-decoration: none;
}

.article-svg {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}

.account-img {
  height: 125px;
  width: 125px;
  margin-right: 20px;
  margin-bottom: 16px;
}

.account-heading {
  font-size: 2.5rem;
}
```

how to link css file in "base.html" file  
```html 
  <link href="{% static 'blog/main.css' %}" rel="stylesheet" type="text/css">
```

to load static add following code for on the top of "base.html" file  
```html 
{% load static %}  
```

open "home.html" template and modify posts using following html   
```html 
<article class="media content-section">
  <div class="media-body">
    <div class="article-metadata">
      <a class="mr-2" href="#">{{ post.author }}</a>
      <small class="text-muted">{{ post.date_posted }}</small>
    </div>
    <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
    <p class="article-content">{{ post.content }}</p>
  </div>
</article>
```

show how to use Django url tags for navigation with "base.html" template.  
```html
    <!--<a class="nav-item nav-link" href="/">Home</a>-->
    <a class="nav-item nav-link" href="{% url 'blog-home' %}">Home</a>
    <!--<a class="nav-item nav-link" href="/about">About</a>-->
    <a class="nav-item nav-link" href="{% url 'blog-about' %}">About</a>
```        

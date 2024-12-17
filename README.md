# Login and Logout System   

let's see how to build login system for who don't have "admin" access.  
first see how to do that using default builtin login view.  
builtin "LoginView" and "LogoutView" are "class-based" views.   
builtin views not handle the templates and handle like logic, forms etc.   

> django_project/django_project/urls.py  
```py 
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib import views as auth_views # add here  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', user_views.register, name='register'), 
    # as_view(template_name='users/login.html') meain where to view template file
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), 
]
```

to create "login.html" template make copy from "register.html" and make changes.  
> django_project/users/templates/users/login.html  
```html 
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Log In</legend>
          {{ form | crispy }}
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Login</button>
      </div>
    </form>
    <div class="border-top pt-3">
      <small class="text-muted">
        Need an account? <a class="ml-2" href="{% url 'register' %}">Sign Up Now</a>
      </small>
    </div>
  </div>
{% endblock content %}
```

after "login" from login page we can see it redirect "profile" that not existed.  
we can change/overwrite redirec path using "settings.py" file in following way.  
>django_project/django_project/settings.py  
```
# under page is good to write following setting  
LOGIN_REDIRECT_URL = 'blog-home'
```

let's change redirect route after register from "blog-home" to "login"  
```py 
    return redirect('login')
```

let's create "logout" route by copying "register.html" template to "logout.html" template  
```py 
{% extends "blog/base.html" %}
{% block content %}
    <h2>You have been logged out </h2>
    <div class="border-top pt-3">
      <small class="text-muted">
        <a class="ml-2" href="{% url 'login' %}">Log In Again</a>
      </small>
    </div>
{% endblock content %}
```

you can't access above 'localhost:8000/logout' route direcly from browser because of GET request not allow for "logout" route.  
add following "POST" method to "base.html" file near "Register" link.  
>django_project/blog/templates/blog/base.html  
```html 
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-link">Log Out</button>
</form>
```

let's set "login" and "register" urls according to is login or not.  
>django_project/blog/templates/blog/base.html  
```html 
    <div class="navbar-nav">
      {% if user.is_authenticated %}
        <form method="post" action="{% url 'logout' %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-link">Log Out</button>
        </form>
      {% else %}
        <a class="nav-item nav-link" href="#">Login</a>
        <a class="nav-item nav-link" href="#">Register</a>
      {% endif %}
    </div>
```

let's see how to add protected/restriction rountes.  
> django_project/users/views.py  
```py 
from django.contrib.auth.decorators import login_required

@login_required # add decorators for required login user
def profile(request):
    return render(request, 'users/profile.html')
```

> django_project/users/templates/users/profile.html  
```html 
{% extends "blog/base.html" %}
{% block content %}
  <h1>{{ user.username}}</h1>
{% endblock content %}
```

> django_project/django_project/urls.py  
```py 
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'), 
    path('profile/', user_views.profile, name='profile'), # add here  
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'), 
    path('', include('blog.urls')),
]
```

> django_project/blog/templates/blog/base.html  
```html 
    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
```

show how to redirect proteced route if user not loggedin and after redirect original route like callback url.     
> django_project/django_project/settings.py  
```py 
# go down to the settings file  
LOGIN_URL = 'login'
```

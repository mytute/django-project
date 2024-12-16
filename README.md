# User Registration          

for user auth best thing is create new app inside our project. 

goto directory where located "manage.py" and run following cmd   
```bash 
$ python manage.py startapp users  
```

when we create new app  add installed apps list in project "settings.py" file.  
>django_project/django_project/settings.py  
```python
INSTALLED_APPS = [
    'users.apps.UsersConfig', # add here  
    'blog.apps.BlogConfig',
    ...
]
```

go to "views.py" file and create register view.  
Django already has built in "UserCreationForm" and just import it.  
>django_project/users/views.py  
```py 
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  # import builtin auth form  

def register(request): 
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form', form})
```

now we need to create a template for "users/register.html" that you add above.  
> django_project/users/templates/users/register.html  
```html 
{% extends "blog/base.html" %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      <!--here add CSRF(cross site request forgery) token for protect form from certain attacts   -->
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Join Today</legend>
          {{ form }}
          <!--{{ form.as_p }} this render tags to paragrahp tags -->
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Sign Up</button>
      </div>
    </form>
    <div class="border-top pt-3">
      <small class="text-muted">
        Already have an account? <a class="ml-2" href="#">Sign In</a>
      </small>
    </div>
  </div>
{% endblock content %}
```

now we have to create route for browser navigation on "django_project/django_project/urls.py".  
( in our blog application we create a urls module inside blog and import it in to main urls.py file)  
```py 
from django.contrib import admin
from django.urls import path, include
from users import views as user_views # add here  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', user_views.register, name='register'),# add here    
]
```

change "register" route for grap the "POST" request. By default it grap "GET" requests.  
> django_project/users/views.py  
```py 
from django.shortcuts import redirect, render # add "render"
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages # add "messages"

# update following register function for read "POST" request.  
def register(request): 
    # for POST request   
    if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
          form.save() # hash password and save user form on database.     
          username = form.cleaned_data.get('username')
          messages.success(request, f'Account created for {username}')
          return redirect('blog-home')
    # for GET request  
    else: 
      form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
```

for "base.html" template add following lines for showing flash message.  
> django_project/blog/templates/blog/base.html  
```html 
  {% if messages %}
    {% for message in messages %}
    <div class="alert alert-{{message.tags}}">
      {{ message }}
    </div>
    {% endfor %}
  {% endif %}
  <!--add above to content block line -->
  {% block content %}{% endblock %} 
```

type of flash message that django can send to browser.  
messages.debug
messages.info
messages.success
messages.warning
messages.error

let's add custom fields to form on "register" template.  
for that we have to create new form that inherite with "form".  
create new file "form.py" inside "users" directory.  
django_project/users/forms.py    
```py 
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  

# class inherite by "UserCreationForm"
class UserCreationForm(UserCreationForm):
    email = forms.EmailField() # (required=False) if optional 

    
    class Meta:
        model = User # validate with "User" model and save on "User" table   
        fields = ['username', 'email', 'password1', 'password2'] #  define display order of fields 
```

let's import created new form in to "register" route view.   
```py 
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import UserRegisterForm # add here  

def register(request): 
    if request.method == 'POST':
      form = UserRegisterForm(request.POST) # update here 
      if form.is_valid():
          form.save() 
          username = form.cleaned_data.get('username')
          messages.success(request, f'Account created for {username}')
          return redirect('blog-home')

    else: 
      form = UserRegisterForm() # update here 
    return render(request, 'users/register.html', {'form': form})
```

we don't need all of this validation information so large.  
Adding classes to our form fields is not good for external customization.  
Better we can all of that within our template. for that we use third-party Django application call "crispy forms".  
Frist we need to install crispy forms  
```bash 
$ pip install django-crispy-forms  
$ pip install crispy-bootstrap5
```

above added application need to add "INSTALLED_APPS" list in settings.py file  
```py 
INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'crispy_forms', # add here  
    "crispy_bootstrap5", # add here 
    # ... 
]


# styles lib for crispy-forms  
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

load crispy where we need to load it and set pipe to form with crispy  
```html 
{% extends "blog/base.html" %}
<!--add here -->
{% load crispy_forms_tags %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      <!--here add CSRF(cross site request forgery) token for protect form from certain attacts   -->
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Join Today</legend>
          <!--{{ form }}-->
          <!--pipe here-->
          {{ form | crispy }}

      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Sign Up</button>
      </div>
    </form>
    <div class="border-top pt-3">
      <small class="text-muted">
        Already have an account? <a class="ml-2" href="#">Sign In</a>
      </small>
    </div>
  </div>
{% endblock content %}
```

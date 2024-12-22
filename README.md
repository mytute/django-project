# Email and Password Reset      

Django has instructions for a user to reset their password.  

> django_project/django_project/urls.py  
```py 
from django.contrib import admin
from django.forms.widgets import static
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views  

from django.conf import settings # add here
from django.conf.urls.static import static  # add here  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'), 
    path('profile/', user_views.profile, name='profile'), 
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), 
    
    # add from here 
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'), 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'), 
    path('', include('blog.urls')),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'), 
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'), 
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'), 
]
```

next you have to create template for above "reset-password", "password_reset_done", "password_reset_confirm" and "password_reset_complete" templates.     
> django_project/users/templates/users/password_reset.html  
```py 
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Reset Password</legend>
          {{ form | crispy }}
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Request Password Reset</button>
      </div 
    </form>
  </div>
{% endblock content %}
```

> django_project/users/templates/users/password_reset_done.html  
```py 
{% extends "blog/base.html" %}
{% block content %}
    <div class="alert alert-info">
      An email has been sent with instructions to reset your password  
    </div>
{% endblock content %}
```

> django_project/users/templates/users/password_reset_confirm.html  
```py 
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Reset Password</legend>
          {{ form | crispy }}
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Reset Password</button>
      </div 
    </form>
  </div>
{% endblock content %}
```

> django_project/users/templates/users/password_reset_complete.html  
```py 
{% extends "blog/base.html" %}
{% block content %}
    <div class="alert alert-info">
      Your password has been set.  
    </div>
    <a href="{% url 'login' %}">Sign In here</a>
{% endblock content %}
```


add email details in to end of the settings.py page.  
> 
```py 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True
EMAIL_HOST_USER =  'devmius@gmail.com' #os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = 'nizo trsf bwgx mspo'  #os.environ.get('EMAIL_PASS')

```

you can add password-reset url to login page.  
```html 
  <div class="form-group">
    <button class="btn btn-outline-info" type="submit">Login</button>
    <!--add here -->
    <small class="text-muted ml-2">
      <a href="{% url 'password_reset' %}">Forgot Password?</a>
    </small>
  </div>
```

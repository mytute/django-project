# Update User Profile       

In order to update user profile we need to have forms.  

let's assume we need to update "username", "email" and "image" fileds.  
because of "image" field in "Profile" model we need to do it seperatly.  

>django_project/user/forms.py  
```py 
form django import forms
from django.contrib.auth.models import User  
from .models import Profile  

# for update "username" and "email"
class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField() # additional field that we added  

  class Meta:
    model = User
    fields = ['username', 'email']

# for update "image" filed
class ProfileUpdateForm(forms.ModelForm):

  class Meta:
    model = Profile 
    fields = ['image']

```

let's add above forms to "views.py" file.   
>django_project/user/views.py    
```py 
from .forms import UserUpdateForm, ProfileUpdateForm  


@login_required
def profile(request):
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()  
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
```

let's go to "profile.html" to add forms to update.   
in the form "enctype="multipart/form-data"" for sending file data.  
> django_project/users/templates/users/profile.html  
```html 
{% extends "blog/base.html" %}
 <!--need to load crispy forms when it is in the tempalte-->
{% load crispy_forms_tags %}
{% block content %}
 <div class="content-section">
  <div class="media">
    <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
    <div class="media-body">
      <h2 class="account-heading">{{ user.username }}</h2>
      <p class="text-secondary">{{ user.email }}</p>
    </div>
  </div>
  <!-- just copy from register form -->
    <form method="POST" enctype="multipart/form-data">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Profile Info</legend>
          {{ u_form | crispy }}
          {{ p_form | crispy }}
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Update</button>
      </div>
    </form>
 </div>
{% endblock content %}
```

let's set logic when update user/profile data with POST request. 
> django_project/users/views.py
```py 
@login_required
def profile(request):
    # u_form = UserUpdateForm() load emty form 
    # p_form = ProfileUpdateForm() load emty form  

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # for read file we have to put "request.FILES" argument.  
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # if save successfully need to redireact profile to see updated values.  
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
```


let's see how to resize uploading image with "Pillow".  
here we are going to overrite save function in the model.  
> django_project/users/models.py  
```py 
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        # get image path to pillow class 
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
             # resize the image.   
            img.thumbnail(output_size)
            # save resized image 
            img.save(self.image.path)
``` 

go to "post.html" tempalte and add image for author  
```html 
{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
      <article class="media content-section">
         # add here 
        <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}"
        <div class="media-body">
          <div class="article-metadata">
            <a class="mr-2" href="#">{{ post.author }}</a>
            <!--change date format that direcly getting from database-->
            <small class="text-muted">{{ post.date_posted|date:"F d, Y" }}</small>
          </div>
          <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
          <p class="article-content">{{ post.content }}</p>
        </div>
      </article> 
    {% endfor %}
{% endblock content %}
```

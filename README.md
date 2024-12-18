# User Profile and Picture     

Here we will work on our profile page and upload profile image. also use of Django signals.  

we have to add field to buildin "User" model 

to save image on database you have to use lib call "Pillow"  
```bash 
$ pip install Pillow
```

create model for "Profile" because in "User" models can't add field for image.  
> django_project/users/models.py 
```py 
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # create one-to-one relationship with user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # upload_to : directory to store profile image.   
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
```

run migration for new model.  
```bash 
$ python manage.py makemigrations  
$ python manage.py migrate  
```

let's register new model with   
> django_project/users/admin.py  
```py
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

go to "localhost/admin" and add profile image from admin panel.  

using bash/shell we can access that model and check the database model values.  
```bash 
$ python mange.py shell 
>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username='samadhi').first()
>>> user.profile.image
<ImageFieldFile: profile_pics/mx7-11.jpg>
>>> user.profile.image.width
1024
>>> user.profile.image.url
'/profile_pics/mx7-11.jpg'
>>> user2= User.objects.filter(username='samadhilak').first()
>>> user2.profile.image
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/home/swashi/.local/lib/python3.13/site-packages/django/db/models/fields/related_descriptors.py", line 531, in __get__
    raise self.RelatedObjectDoesNotExist(
    ...<2 lines>...
    )
django.contrib.auth.models.User.profile.RelatedObjectDoesNotExist: User has no profile.
```

you can see uploaded image in following directory(project root directory)      
>django_project/profile_pics/image_file_name.jpg  

let's change image saving directory.  
> django_project/django_project/settings.py  
```py 
# MEDIA_ROOT is the location that where uploaded file located in file system.  
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
# MEDIA_URL is the public url of above directory  
MEDIA_URL = '/media/'
```

go to admin and delete created profiles and re-upload the image using admin panel.   
and you can see uploaded image in following directory.  
> django_project/media/profile_pics/image_file_name.jpg  

show how to set default image automatically when create new user using "signals"  
inside "users" folder create file name "signals.py"  
> django_project/users/singals.py  
```py 
# import signal that emit after database did save  
from django.db.models.signals import post_save 
from django.contrib.auth.models import User 
from django.dispatch import receiver  # for receiver function 
from .models import Profile  

# function for get creating User for save on Profile.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
      Profile.objects.create(user=instance)


# function for save new profile value
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
  instance.profile.save()
```
next you have to import above signals on 
> django_project/users/app.py  
```py 
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # add following "ready" function.   
    def ready(self):
        import users.signals
```

now you can see default image set for on the browser for newly created user.  
```html 
    <img class="rounded-circle account-img" src="/media/default.jpg">
    <div class="media-body">
      <h2 class="account-heading">pasindu001</h2>
      <p class="text-secondary">tisa@gmail.com</p>
    </div>
  
```


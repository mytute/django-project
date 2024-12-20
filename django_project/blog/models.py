from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # import user model  
from django.urls import reverse

class Post(models.Model): 
    title = models.CharField(max_length= 100)
    content = models.TextField()
    # auto_now_add=True auto add date when row created(only one time)
    # auto_now=True auto update when update row  
    # default=timezone.now ??
    date_posted = models.DateTimeField(default= timezone.now)
    # add foreign key for one to many relationship ( one user can have multiple posts)   
    # on_delete : when user deleted the it will delete posts as well   
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or "Untitled Post"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

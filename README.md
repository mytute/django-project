# Database and Migrations        

Jango has its own built-in ORM(Object Relational Mapper).   
ORM allows us to access our database and easy to use object oriented way.  
you can use different databases without changing your code.  
great thing about the django ORM is we can represent our database structure as classes which call "models".  
Django already created "model.py" file inside "blog" directory.  


if we didn't have a way to run migrations then we have to run some complicated SQL to update our database structure for did't mess with current data.  


create database model in "models.py" file  
>django_project/blog/models.py  
```py 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # import user model  

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
```

then run the migrations commands to sync database  
```bash 
$ python manage.py makemigrations  
# before run migration cmd good to check sql code using below way   
$ python manage.py migrate  
```

check migrations file that created after run above codes.  
> django_project/blog/migrations/0001_initial.py  

show how to see sql code that created from ORM by using migration number  
```bash 
#  blog: application name, 0001: migration number   
$ python manage.py sqlmigrate blog 0001  

# result  
BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "content" text NOT NULL, "date_posted" datetime NOT NULL, "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
COMMIT;
```

show how to run Django python shell for work with models  
```bash 
$ python manage.py shell   
```

let import both post model and user models  
```python  
>>> from blog.models import Post  
>>> from django.contrib.auth.models import User  

# see all the data of the User table  
>>> User.objects.all()  
# <QuerySet [<User: samadhi>]>

# see first/last record 
>> User.objects.first()  
>> User.objects.last()  
# <User: samadhi>

# filter records  
>> User.objects.filter(username='samadhi')
# <QuerySet [<User: samadhi>]>

# filter records and select first record   
>> User.objects.filter(username='samadhi').first()
# <User: samadhi>

# filter record and store result to variable  
>> user = User.objects.filter(username='samadhi').first()
>> user  
# <User: samadhi>
>> user.id  # get user id  
# 1 
>> user.pk  # get user primary key  
# 1

# select user by id  
>> user = User.objects.get(id=1)
>> user  
# <User: samadhi>

# let's check the post  
>> Post.objects.all()  
# <QuerySet []>

# let's create a post by using user variable   
# first need to create quary  
>> post_1 = Post(title='blog 1', content='First Post Content!', author=user)
# then run the query by call save method.  
>> post_1.save()
>> Post.objects.all()  
# <QuerySet [<Post: Post object (1)>]>
# above Post result is not much discriptive. make discriptive by using dunder STR method.  
```

let's add dunder str method to Post model.  
```py 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  

class Post(models.Model): 
    title = models.CharField(max_length= 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
     return self.title or "Untitle Post" 
```

continue with bash  
```python 
# update above changes first exit  
>> exit() 
# rerun python shell cmd  
>> python manage.py shell  
# reimport post and user models  
>>> from blog.models import Post  
>>> from django.contrib.auth.models import User  

# let's check post list    
>> Post.objects.all()
# <QuerySet [<Post: blog 1>]>

# let' create new post  
>> user = User.objects.filter(username='samadhi').first()
>> post_2 = Post(title='blog 2', content='Second Post Content!', author=user)
# same we can add user by id to the post
# >> post_2 = Post(title='blog 2', content='Second Post Content!', author_id=user_id)
>> post_2.save()

# select post and check post object values  
>> post = Post.objects.first()  
>> post.content # 'First Post Content!' 
>> post.date_posted # datetime.datetime(2024, 12, 10, 22, 31, 38, 681675, tzinfo=datetime.timezone.utc) 
>> post.author # <User: samadhi>
>> post.author.email # 'samadhivkcom@gmail.com'

# get all the post written by specific user  
# normal way is select user and get post of user from post table. but in django has special way using ".modelname_set"  
>> user.post_set  # not readable  
>> user.post_set.all()

# we can create a post directly using above post_set with user model(here no need to run .save() method )
>> user.post_set.create(title='blog 3', content='Third Post Content!')
>> Post.objects.all() # <QuerySet [<Post: blog 1>, <Post: blog 2>, <Post: blog 3>]> 

>> exit()  
```

show how to replace "posts" static object with database post values  
> django_project/blog/views.py  
```py 
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post # import post model from same directory  

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
            # 'posts':posts
            'posts': Post.objects.all() # change here.  
            }
    return render(request, 'blog/home.html', context)   
```

show how to change date format in the html using django doc.  
> django_project/blog/templates/blog/home.html  
```home.html
{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
      <article class="media content-section">
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

what to do see "Post" model in admin panel in django  
for that you have to register the model in to "admin.py" file  
> django_project/blog/admin.py  
```py 
from django.contrib import admin
from .models import Post # import the model that you need to  

admin.site.register(Post) # resiter post model here
```

by clicking Post mode in Django admin try to make CRUD posts 

# Pagination    

let's add posts from json data to the Post table.  

```bash 
$ python manage.py shell  
>>> import json  
>>> from blog.models import post 
>>> with open('posts.json') as f:
...  post_json = json.load(f)

>>> for post in post_json:
      post = Post(title=post['title'], content=post['content'], author_id=post['user_id'])
      post.save()  
>>> exit()  
```

for paginate posts we can use paginate object.  
let's see about how Paginator object is going to work.   
```bash 
$ python manage.py shell  
>>> from django.core.paginator import Paginator  
>>> posts = ['1', '2', '3', '4', '5']
>>> p = Paginator(posts, 2)
>>> p.num_pages  
3  
>>> for page in p.page_range:
...    print(page)
>>> p1 = p.page(1)  
>>> p1  
<Page 1 of 3>
>>> p1.number   
1 
>>> p1.object_list  
['1', '2']
>>> p1.has_previous()  
False  
>>> p1.have_next()  
True  
>>> p1.next_page_number()  
2  
```

we are going to add pagination for "home" page.   
if we using class list view then no need to define pagination object there.  
just need to add attribute call "paginate_by"
> django_prroject/blog/views.py  
```py 
class PostListView(ListView):
  model= Post
  template_name = 'blog/home.html' 
  context_object_name = 'posts'
  ordering = ['date_posted'] 
  # add here
  paginate_by = 2 # paginate list 2 post for a page.  
```

just check following links by changing page number   
http://localhost:8000/?page=2

let's add linked urls for our webpage to navigate between pages.   
> django_prroject/blog/templates/blog/home.html  
```html 
{% extends "blog/base.html" %}
{% block content %}
    {% for post in posts %}
      <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}"/>
        <div class="media-body">
          <div class="article-metadata">
            <a class="mr-2" href="#">{{ post.author }}</a>
            <!--change date format that direcly getting from database-->
            <small class="text-muted">{{ post.date_posted|date:"F d, Y" }}</small>
          </div>
          <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
          <p class="article-content">{{ post.content }}</p>
        </div>
      </article> 
    {% endfor %}    

    <!--pagination start by here..-->
    {% if is_paginated %}

      {% if page_obj.has_previous %}
        <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
      {% endif %}

      {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
          <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
          <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
        {% endif %}
      {% endfor %}

      {% if page_obj.has_next %}
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
      {% endif %}

    {% endif %}
{% endblock content %}

```

let's see how to filter post under pagination.  
let's implement when click username link load only that user's post under pagination.  
> django_prroject/blog/views.py  
```py 
from django.contrib.auth.models import User

# let's create new list view for filtering pagination view.  
class UserPostListView(ListView):
  model= Post
  template_name = 'blog/user_post.html' 
  context_object_name = 'posts'
  # ordering = ['date_posted']  add this line direcly to overrides query  
  paginate_by = 2 

  def get_queryset(self):
     # return super().get_queryset()
     # way to get query parameter: kwargs.get('username')
     user = get_object_or_404(User, username=self.kwargs.get('username'))
     return Post.objects.filter(author=user).order_by('-date_posted')
```

let's create url pattern in urls.  
```py 
from django.urls import path 
from . import views  
from .views import (
    PostListView, 
    ...
    UserPostListView
)

urlpatterns = [
  path('', PostListView.as_view(), name='blog-home'),
  # add here
  path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/new/', PostCreateView.as_view(), name='post-create'), 
  ...
]
```
 
next create template named "blog/user_post.html" similar to home page.  
> django_prroject/blog/templates/blog/user_post.html  
```html 
{% extends "blog/base.html" %}
{% block content %}
     <!--add user name and total number of post here -->
     <h1 class="mb-3" > Posts by {{ view.kwargs.username }} ({{ page_obj.paginator.count }})</h1>
    {% for post in posts %}
      <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}"/>
        <div class="media-body">
          <div class="article-metadata">
            <!--add href value here to navigate filter route.  -->
            <a class="mr-2" href="{% url 'user-post' post.author.username %}">{{ post.author }}</a>
            <!--change date format that direcly getting from database-->
            <small class="text-muted">{{ post.date_posted|date:"F d, Y" }}</small>
          </div>
          <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
          <p class="article-content">{{ post.content }}</p>
        </div>
      </article> 
    {% endfor %}    
    {% if is_paginated %}

      {% if page_obj.has_previous %}
        <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
      {% endif %}

      {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
          <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
          <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
        {% endif %}
      {% endfor %}

      {% if page_obj.has_next %}
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
      {% endif %}

    {% endif %}
{% endblock content %}
```

change navigation when click the username on browser.  
navigate to filter template url is    
```html 
href="{% url 'user-post' post.author.username %}"
```

now click username of post and check fitering and pagination.  

# Create, Update, and Delete Posts        


we have used function based views and url pattern directed to it then render the remplate.     

let's create class-based view for our homepage. 
listview, createview, updateview and deleteview   

1. listview 

current view  
> django_project/blog/views.py  
```py 
def home(request):
  context = {
      'posts': Post.objects.all()
  }
  return render(request, 'blog/home.html', context)
```

updated list view  
> django_project/blog/views.py  
```py
from django.views,generic import ListView  

class PostListView(ListView):
  # what model to query list this view  
  model= Post
  # changing default looking template by class view.  
  template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
  # we no need to query posts list because "ListView" already include it.  
  context_object_name = 'posts'
  # order post according date.
  ordering = ['-date_posted'] # ['-date_posted'] for des order.  
```

we need to linke new class view from the route.  
and here we need to convert class into an actual view.  
> django_project/blog/urls.py  
```py 
from django.urls import path 
from .views import PostListView
from . import views  


urlpatterns = [
  # path('', views.home, name='blog-home'),
  path('', PostListView.as_view(), name='blog-home'),
  path('about/', views.about, name='blog-about')
]
```

By default class view not looking "home.html" template because for class view there is nameing convention for the template.  
<app>/<model>_<viewtype>.html    
blog/post_list.html  

let's see how to show details of post by using details view.  

> django_project/blog/views.py  
```py 
from django.views,generic import ListView, DetailView 

class PostDetailView(DetailView):
  model= Post


```

then you need to url pattern for view post details.  
> django_project/blog/urls.py  
```py 
from django.urls import path 
from .views import PostListView, PostDetailView
from . import views  

urlpatterns = [
  # path('', views.home, name='blog-home'),
  path('', PostListView.as_view(), name='blog-home'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # add here
  path('about/', views.about, name='blog-about')
]
```

let's create template for above "post-detail" route.  
format of tempalte name : <app>/<model>_<viewtype>.html  
 > django_project/blog/templates/blog/post_detail.html    
 ```py 
{% extends "blog/base.html" %}
{% block content %}
  <article class="media content-section">
    <img class="rounded-circle article-img" src="{{ object.author.profile.image.url }}"/>
    <div class="media-body">
      <div class="article-metadata">
        <a class="mr-2" href="#">{{ object.author }}</a>
        <!--change date format that direcly getting from database-->
        <small class="text-muted">{{ object.date_posted|date:"F d, Y" }}</small>
      </div>
      <h2 class="article-title" />{{ object.title }}</h2>
      <p class="article-content">{{ object.content }}</p>
    </div>
  </article> 
{% endblock content %}
 ```

 now check the url (http://localhost:8000/post/1/)

let's change post-list-view template urls to detail-view.  
go to "home.html" template and pass "post-detail" name with post id     
> django_project/blog/templates/blog/home.html  
```html 
<h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
```

let's see how to create post using "CreateView"  
> django_project/blog/views.py  
```py 
from django.views.generic import ( 
   CreateView, 
   ListView, 
   DetailView 
)

class PostCreateView(CreateView):
  model= Post
  # define field should contain in form 
  fields = ['title', 'content']
```

next create url pattern for create view   
> django_project/blog/urls.py  
```py 
from django.urls import path 
from . import views  
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView # add here 
)

urlpatterns = [
  # path('', views.home, name='blog-home'),
  path('', PostListView.as_view(), name='blog-home'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/new/', PostCreateView.as_view(), name='post-create'), # add here
  path('about/', views.about, name='blog-about')
]
```

now we need to create template for create view.  
for create template naming convention is "post_from.html"  
> django_project/blog/templates/blog/post_form.html   
```html 
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Blog Post</legend>
          {{ form | crispy }}
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Post</button>
      </div>
    </form>
  </div>
{% endblock content %}
```

we need to overrides "form_valid" function to add user to saving post for the author field.  
> django_project/blog/views.py  
```py 
# to privent access of create post who are not loggedin  
from django.contrib.auth.mixins import LoginRequiredMixin 

# if we remove LoginRequiredMixin then user can create post who even not loggedin  
class PostCreateView(LoginRequiredMixin, CreateView):
  model= Post
  # define field should contain in form 
  fields = ['title', 'content']

  # add current user details because it need to save post author field  
  # for that we need overrides "form_valid" method  
  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)
```

after press submit button for create new post we need to set redirect url.   
after submit if we want redirec to newly created post here we can't use "redirect" function because here url is dynamic.   
so here we are going to use function in post model to return new url.    
> django_project/blog/models.py  
```py 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  
from django.urls import reverse # add here

class Post(models.Model): 
    title = models.CharField(max_length= 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or "Untitled Post"

    # add for return newly created url  
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
```

let's see how to update(no need to code tempalte can use create(post_form) template) 

> django_project/blog/views.py  
```py 
from django.views.generic import (
  CreateView, 
  ListView, 
  DetailView, 
  UpdateView # add here  
)

class PostUpdateView(LoginRequiredMixin, UpdateView):
  model= Post
  # define field should contain in form 
  fields = ['title', 'content']

  # add current user details because it need to save post author field  
  # for that we need overrides "form_valid" method  
  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)
```

next create urls route patterns in urls.py file   
> django_project/blog/utls.py  
```py 
from django.urls import path 
from . import views  
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView # add here  
)

urlpatterns = [
  # path('', views.home, name='blog-home'),
  path('', PostListView.as_view(), name='blog-home'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/new/', PostCreateView.as_view(), name='post-create'), 
  path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'), # add here
  path('about/', views.about, name='blog-about')
]
```

next see how to privent update post that create by another user.   
for that we are going to use another mixing call "UserPassesTestMixin"
> django_project/blog/views.py  
 ```py 
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model= Post
  fields = ['title', 'content']

  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)

  # here you need to add function to pass access validation.   
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False
 ```

let's see how to delete post.(this is similar to post details )  
> django_project/blog/views.py  
```py 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model= Post
  success_url = '/' # post will not remove until add redirec url 

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False
```

next you need to have add url pattern in "urls.py" file.  
```py 
from django.urls import path 
from . import views  
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView # add here  
)

urlpatterns = [
  # path('', views.home, name='blog-home'),
  path('', PostListView.as_view(), name='blog-home'),
  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
  path('post/new/', PostCreateView.as_view(), name='post-create'), 
  path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), 
  path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # add here
  path('about/', views.about, name='blog-about')
]
```

next need to create template that show delete confirmation.  
create new template for naming convention "post_confirm_delete.html".  
> django_project/blog/templates/blog/post_confirm_delete.html  
```html 
{% extends "blog/base.html" %}
{% block content %}
  <div class='content-section'>
    <form method="POST">
      {% csrf_token %}
      <fieldset class="form-group">
        <legend class="border-bottom mb-4">Delete Post</legend>
        <h2>Are you sure you want to delete the post "{{object.title}}" ? </h2>
      </fieldset>
      <div class="form-group">
        <button class="btn btn-outline-danger" type="submit">Yes, Delete</button>
        <a class="btn btn-outline-secondary" href="{% url 'post-detail' object.id %}">Cancel</a>
      </div>
    </form>
  </div>
{% endblock content %}
```

post will not delete until you add redirect url.    
let's redirect to homepage inside "PostDeleteView"  
> django_project/blog/views.py  
```py 
success_url = '/'
```

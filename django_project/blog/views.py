from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.http import HttpResponse
from .models import Post
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView  

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
            'posts': Post.objects.all() 
            }
    return render(request, 'blog/home.html', context) # pass data as third parameter   


def about(request):
    # return HttpResponse('<h1>Blog About</h1>')
    return render(request, 'blog/about.html')

# class view instead for "home" here.  
class PostListView(ListView):
  # what model to query list this view  
  model= Post
  # changing default looking template by class view.  
  template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
  # we no need to query posts list because "ListView" already include it.  
  context_object_name = 'posts'
  # order post according date.
  ordering = ['date_posted'] # ['-date_posted'] for des order.  


class PostDetailView(DetailView):
  model= Post


class PostCreateView(LoginRequiredMixin, CreateView):
  model= Post
  # define field should contain in form 
  fields = ['title', 'content']

  # add current user details because it need to save post author field  
  # for that we need overrides "form_valid" method  
  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model= Post
  # define field should contain in form 
  fields = ['title', 'content']

  # add current user details because it need to save post author field  
  # for that we need overrides "form_valid" method  
  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model= Post
  success_url = '/'

  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
        return True
    return False

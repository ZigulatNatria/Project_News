from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm

class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10



class PostDetailView(DetailView):
    template_name = 'news_app/post_detail.html'
    queryset = Post.objects.all()

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # добавим переменную текущей даты time_now
        return context


class PostCreateView(CreateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm



class PostUdateView(UpdateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostDeleteView(DeleteView):
    template_name = 'news_app/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'




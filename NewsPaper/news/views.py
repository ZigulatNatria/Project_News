from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, User, Category, PostCategory, UserCategory
from django.shortcuts import redirect
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



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


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news_app/post_create.html'
    form_class = PostForm

    def post(self, request):
        title = request.POST['title']
        text = request.POST['text']
        post_category_id = request.POST['postCategory']
        category_id = Category.objects.get(id=post_category_id).id
        category_object = Category.objects.get(id=post_category_id)

        if Author.objects.filter(authorUser__username=request.user.username).exists():
            author = Author.objects.get(authorUser__username=request.user.username).id
        else:
            author = Author.objects.create(authorUser=request.user).id
        postt = Post.objects.create(author_id=author, title=title, text=text)
        postt.save()

        new_postcategory = PostCategory.objects.create(postTrough=postt, categoryTrough=category_object)
        new_postcategory.save()

        return redirect('/news/')



class PostUdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news_app/post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news_app/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news_app/author_update.html'
    context_object_name = 'user'
    form_class = UserForm
    success_url = '/'


    def get_object(self, **kwargs):
        return self.request.user


@login_required
def add_subscribe(request):
    user = request.user
    category = Category.objects.get(pk=request.POST['id_cat'])
    subscribe = UserCategory(user_id=user.id, category_id=category.id)
    subscribe.save()
    return redirect('/news/')


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('-id')

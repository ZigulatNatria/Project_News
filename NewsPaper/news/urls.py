from django.urls import path
from .views import PostsList, PostDetailView, PostSearch, PostUdateView,\
    PostDeleteView, PostCreateView, AuthorUpdateView, \
    CategoryList, add_subscribe  # импортируем наше представление


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search', PostSearch.as_view()),
    path('<int:pk>/edit', PostUdateView.as_view(), name='post_create'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('user/', AuthorUpdateView.as_view(), name='author_update'),
    path('sub', CategoryList.as_view(), name='category'),
    path('subscribe/', add_subscribe, name='subscribe')

]
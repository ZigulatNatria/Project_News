from django.forms import ModelForm
from .models import Post, Author, User

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'title',
            'text',
        ]



class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username']

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    """Форма на основе модели Post для создания поста."""

    class Meta:
        model = Post
        exclude = ('author', 'is_published', 'created_at')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    """Форма на основе модели Comment для создания комментария."""

    class Meta:
        model = Comment
        fields = ('text',)


class RegistrationForm(UserCreationForm):
    """Форма на основе модели User для регистрации профиля."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

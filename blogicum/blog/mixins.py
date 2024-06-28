from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from .views import Post
from .models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин проверки авторства объекта."""

    def test_func(self):
        return self.get_object().author == self.request.user


class PostCreateUpdateDeleteMixin():
    """Миксин модели Post."""

    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class CommentCreateUpdateDeleteMixin():
    """Миксин модели Comment."""

    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.kwargs.get('post_id'),))

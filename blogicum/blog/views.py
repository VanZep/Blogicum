from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, User
from .forms import PostForm, CommentForm
from .mixins import (
    OnlyAuthorMixin,
    PostCreateUpdateDeleteMixin,
    CommentCreateUpdateDeleteMixin
)
from .utils import (
    add_select_related_to_queryset,
    add_filter_to_queryset,
    add_annotate_and_orderby_to_queryset
)
from .constants import NUMBER_OF_POSTS


class PostListView(ListView):
    """Класс представления списка постов.
    Главная страница: index
    """

    model = Post
    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS

    def get_queryset(self):
        return add_select_related_to_queryset(
            add_filter_to_queryset(
                add_annotate_and_orderby_to_queryset(
                    self.model.objects
                )
            )
        )


class PostDetailView(DetailView):
    """Класс представления одного поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            add_select_related_to_queryset(self.model.objects),
            pk=self.kwargs.get(self.pk_url_kwarg)
        )
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            add_select_related_to_queryset(
                add_filter_to_queryset(self.model.objects)
            ),
            pk=self.kwargs.get(self.pk_url_kwarg)
        )

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            form=CommentForm(),
            comments=self.object.comments.select_related('author')
        )


class PostCreateView(
    PostCreateUpdateDeleteMixin, LoginRequiredMixin, CreateView
):
    """Класс представления создания поста."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Класс представления изменения поста."""

    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.kwargs.get(self.pk_url_kwarg))


class PostDeleteView(
    PostCreateUpdateDeleteMixin, OnlyAuthorMixin, DeleteView
):
    """Класс представления удаления поста."""

    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            form=PostForm(
                instance=get_object_or_404(
                    self.model,
                    pk=self.kwargs.get(self.pk_url_kwarg)
                )
            )
        )


class CommentCreateView(
    CommentCreateUpdateDeleteMixin, LoginRequiredMixin, CreateView
):
    """Класс представления создания комментария."""

    post_obj = None
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            pk=kwargs.get(self.pk_url_kwarg)
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentUpdateView(
    CommentCreateUpdateDeleteMixin, OnlyAuthorMixin, UpdateView
):
    """Класс представления изменения комментария."""

    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(
    CommentCreateUpdateDeleteMixin, OnlyAuthorMixin, DeleteView
):
    """Класс представления удаления комментария."""

    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CategoryPostsView(ListView):
    """Класс представления списка постов категории."""

    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    paginate_by = NUMBER_OF_POSTS

    def get_object(self):
        return get_object_or_404(
            self.model,
            is_published=True,
            slug=self.kwargs.get(self.slug_url_kwarg)
        )

    def get_queryset(self):
        return add_select_related_to_queryset(
            add_filter_to_queryset(
                add_annotate_and_orderby_to_queryset(self.get_object().posts)
            )
        )

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            category=self.get_object()
        )


class ProfileListView(ListView):
    """Класс представления профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS

    def get_object(self):
        return get_object_or_404(
            self.model,
            username=self.kwargs.get('username')
        )

    def get_queryset(self):
        user = self.get_object()
        if user == self.request.user:
            return add_select_related_to_queryset(
                add_annotate_and_orderby_to_queryset(user.posts)
            )
        return add_select_related_to_queryset(
            add_filter_to_queryset(
                add_annotate_and_orderby_to_queryset(user.posts)
            )
        )

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            profile=self.get_object()
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления изменения профиля пользователя."""

    model = User
    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'username', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})

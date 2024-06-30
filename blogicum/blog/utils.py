from django.db.models import Count
from django.utils import timezone


def add_select_related_to_queryset(obj):
    """Функция получения списка постов."""
    return obj.select_related(
        'location', 'author', 'category'
    )


def add_filter_to_queryset(obj):
    """Функция получения списка постов с фильтрацией."""
    return obj.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def add_annotate_and_orderby_to_queryset(obj):
    """Функция получения упорядоченного списка постов
    с фильтрацией и количеством комментариев.
    """
    return obj.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

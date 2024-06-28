from django.utils import timezone
from django.db.models import Count


def get_post_list(obj):
    """Функция получения списка постов."""
    return obj.select_related(
        'location', 'author', 'category'
    )


def get_post_list_with_filter(obj):
    """Функция получения списка постов с фильтрацией."""
    return get_post_list(obj).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def get_post_list_with_filter_annotate_orderby(obj):
    """Функция получения упорядоченного списка постов
    с фильтрацией и количеством комментариев.
    """
    return get_post_list_with_filter(obj).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def get_post_list_with_annotate_orderby(obj):
    """Функция получения упорядоченного списка постов
    с количеством комментариев.
    """
    return get_post_list(obj).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

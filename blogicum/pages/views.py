from django.views.generic import TemplateView
from django.shortcuts import render
from django.http.response import (
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
)


class About(TemplateView):
    """Класс представления страницы 'О сайте'."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """Класс представления страницы 'Правила сайта'."""

    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    """403: ошибка проверки CSRF, запрос отклонён."""
    return render(
        request,
        'pages/403csrf.html',
        status=HttpResponseForbidden.status_code
    )


def page_not_found(request, exception):
    """Ошибка 404: страница не найдена."""
    return render(
        request,
        'pages/404.html',
        status=HttpResponseNotFound.status_code
    )


def server_error(request):
    """Ошибка 500: сервер не отвечает."""
    return render(
        request,
        'pages/500.html',
        status=HttpResponseServerError.status_code
    )

from django.db import models

from blog.constants import CHARFIELD_MAX_LENGTH


class PublishedModel(models.Model):
    """Абстрактная модель. Добавляет поле is_published."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет поле created_at."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class PublishedCreatedModel(PublishedModel, CreatedModel):
    """Абстрактная модель. Добавляет поля: is_published, created_at."""

    class Meta:
        abstract = True


class TextModel(models.Model):
    """Абстрактная модель. Добавляет поле text."""

    text = models.TextField(
        verbose_name='Текст'
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    """Абстрактная модель. Добавляет поле title."""

    title = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH,
        verbose_name='Заголовок'
    )

    class Meta:
        abstract = True


class TitleTextModel(TitleModel, TextModel):
    """Абстрактная модель. Добавляет поля: title, text."""

    class Meta:
        abstract = True

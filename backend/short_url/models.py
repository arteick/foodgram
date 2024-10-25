from django.db import models

from utils.services import shorten_url


class ShortUrl(models.Model):
    """Модель для хранения коротких ссылок"""

    full_url = models.URLField(
        'Полная ссылка',
        unique=True)
    short_url = models.CharField(
        'Короткая ссылка',
        unique=True, db_index=True,
        max_length=20, blank=True
    )
    is_active = models.BooleanField(
        'Активна', default=True)
    created_at = models.DateTimeField(
        'Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Таблица ссылок'
        ordering = ('-created_at',)
        unique_together = ('full_url', 'short_url')

    def __str__(self) -> str:
        return f'{self.full_url}'

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    username = models.CharField(
        'Никнейм',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator],
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    avatar = models.ImageField(
        verbose_name='Фото профиля',
        upload_to=('users/images/'),
        blank=True,
        null=True,
        default=None
    )
    password = models.CharField('Пароль', max_length=128)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('email', 'username')


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='Кто подписан',
        on_delete=models.CASCADE, related_name='subscriptions'
    )
    following = models.ForeignKey(
        CustomUser, verbose_name='На кого подписан',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('following', 'user')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='subscribe_yourself_constraint',
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'

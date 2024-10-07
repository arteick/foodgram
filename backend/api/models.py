from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import constants


class CustomUser(AbstractUser):
    email = models.CharField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    username = models.CharField(
        verbose_name='Никнейм',
        unique=True,
        max_length=constants.MAX_LENGTH_150
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.MAX_LENGTH_150,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.MAX_LENGTH_150,
        blank=False
    )
    avatar = models.ImageField(
        verbose_name='Фото профиля',
        upload_to=('users/images/'),
        blank=True
    )
    password = models.CharField('Пароль', max_length=128)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('email', 'username')


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        unique=True,
        max_length=constants.MAX_LENGTH_32
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=constants.MAX_LENGTH_32,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=constants.MAX_LENGTH_128
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=constants.MAX_LENGTH_64,
        help_text=(
            'Единица измерения продукта. '
            'Необходимо ввести сокращённое название.'
        )
    )

    class Meta:
        verbose_name = _('ingridient')
        verbose_name_plural = _('ingridients')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        unique=True,
        max_length=constants.MAX_LENGTH_256
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to=('recipes/images/')
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    ingridients = models.ManyToManyField(
        Ingridient, verbose_name='Ингридиенты',
        through='RecipeIngridient')
    pub_date = models.DateTimeField(
        'Дата публикации рецепта', auto_now_add=True
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ["-pub_date", "id"]
        unique_together = ('author', 'name')

    def __str__(self):
        return self.name


class RecipeIngridient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE, verbose_name='Ингридиент'
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('recipe', 'ingridient')
        default_related_name = 'ingridients_in_recipe'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='Кто добавил в избранное',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт в избранном',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
        default_related_name = 'favorites'

    def __str__(self):
        return self.recipe


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='Кто добавил в корзину',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт в корзине',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        default_related_name = 'in_cart'

    def __str__(self):
        return self.recipe


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser, verbose_name='Кто подписан',
        on_delete=models.CASCADE, related_name='subscriptions'
    )
    user = models.ForeignKey(
        CustomUser, verbose_name='На кого подписан',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        unique_together = ('subscriber', 'user')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('user')),
                name='subscribe_yourself_constraint'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'

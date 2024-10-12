from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        unique=True,
        max_length=32
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=32,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        max_length=128
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64,
        help_text=(
            'Единица измерения продукта. '
            'Необходимо ввести сокращённое название.'
        )
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        unique=True,
        max_length=256
    )
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to=('recipes/images/'),
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги',
        through='RecipeTag'
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингридиенты',
        through='RecipeIngredient'
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта', auto_now_add=True
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ["-pub_date", "id"]
        unique_together = ('author', 'name')

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE, verbose_name='Тег'
    )

    class Meta:
        unique_together = ('recipe', 'tag')
        default_related_name = 'tags_in_recipe'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE, verbose_name='Ингридиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        default_related_name = 'ingredients_in_recipe'


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
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'

    def __str__(self):
        return self.recipe


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name='Кто добавил в корзину',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт в корзине',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзина'
        default_related_name = 'in_cart'

    def __str__(self):
        return self.recipe

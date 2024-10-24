# Generated by Django 4.2.16 on 2024-10-22 15:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'Избранное',
                'default_related_name': 'favorites',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название продукта')),
                ('measurement_unit', models.CharField(help_text='Единица измерения продукта. Необходимо ввести сокращённое название.', max_length=64, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название рецепта')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Фото блюда')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации рецепта')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date', 'id'],
                'default_related_name': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
            options={
                'default_related_name': 'ingredients_in_recipe',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'default_related_name': 'tags_in_recipe',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название тега')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', max_length=32, unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт в корзине')),
            ],
            options={
                'verbose_name': 'корзина',
                'verbose_name_plural': 'Корзина',
                'default_related_name': 'shopping_cart',
            },
        ),
    ]

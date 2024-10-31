import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from users.models import Subscription

User = get_user_model()

classnames = {
    "Ingredient": Ingredient, "Tag": Tag,
    "User": User, "Subscription": Subscription, "Recipe": Recipe,
    "Favorite": Favorite, "Cart": ShoppingCart, "Ri": RecipeIngredient,
    "Rt": RecipeTag
}


class Command(BaseCommand):
    help = """Загружает фикстуры по относительному пути.
    Только теги и ингредиенты"""

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help="путь до файла")
        parser.add_argument('classname', type=str, help="имя модели")

    def handle(self, *args, **kwargs):
        filepath = kwargs.get('filepath')
        name = kwargs.get('classname').lower().capitalize()
        model = classnames.get(name)
        counter = 0

        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            if model == User:
                data['password'] = make_password(data['password'])
            else:
                for item in data:

                    instance = model(**item)
                    instance.save()
                    counter += 1
            print(f'Было создано объектов: {counter}')

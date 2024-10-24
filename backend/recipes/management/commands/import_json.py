import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

classnames = {"Ingredient": Ingredient, "Tag": Tag}


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
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                instance = model(**item)
                instance.save()

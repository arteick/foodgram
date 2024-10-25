from django.utils.crypto import get_random_string
from utils.constants import RANDOM_STRING_CHARS, TOKEN_LENGTH


def shorten_url() -> str:
    """Возвращает случайную строку для короткой ссылки"""
    return get_random_string(TOKEN_LENGTH, RANDOM_STRING_CHARS)


def create_cart_txt(content: list):
    """
    Создаёт текстовый документ для корзины покупок.
    Возвращает файл в режиме чтения.
    """
    cart: dict = {}
    for item in content:
        ingredient_name = item.get('ingredient__name')
        amount = item.get('amount')
        measurement_unit = item.get('ingredient__measurement_unit')
        if cart.get(ingredient_name):
            cart[ingredient_name][0] += amount
            continue
        cart[ingredient_name] = [amount, measurement_unit]

    with open('shopping.txt', 'w') as f:
        for item in cart:
            f.write(f'{item} -> {cart[item][0]} {cart[item][1]}\n')

    return open('shopping.txt', 'r')

from rest_framework.pagination import PageNumberPagination


class PageNumberAndLimit(PageNumberPagination):
    """
    Класс пагинации, поддреживает изменения кол-ва объектов на странице
    с помощью параметра запроса 'limit'
    """
    page_size_query_param = 'limit'

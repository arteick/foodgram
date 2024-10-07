from rest_framework.pagination import PageNumberPagination


class PageNumberAndLimit(PageNumberPagination):
    page_size_query_param = 'limit'

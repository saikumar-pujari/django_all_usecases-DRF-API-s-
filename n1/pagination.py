from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination, CursorPagination)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'paaa'
    max_page_size = 100
    last_page_strings = ('last', 'fuck')


class limitpagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'mylimit'
    offset_query_param = 'myoffset'
    max_limit = 20


class cusrsorpaginaton(CursorPagination):
    page_size = 10
    ordering = 'name'

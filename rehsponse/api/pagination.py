from rest_framework import pagination


class StandardResultsPaginations(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 2000

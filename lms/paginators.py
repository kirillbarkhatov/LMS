from rest_framework.pagination import PageNumberPagination


class TwoItemsPaginator(PageNumberPagination):
    """Типовой пагинатор для постраничного вывода по 2 элемента"""

    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100
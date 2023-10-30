from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Кастомный пагинатор для вывода определенного количества страниц."""

    page_size_query_param = "limit"

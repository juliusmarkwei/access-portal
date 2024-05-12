from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class AccessKeyPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = "page_size"  # Customize the query parameter for page size
    max_page_size = 10  # Set the maximum page size

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
            status=status.HTTP_200_OK,
        )

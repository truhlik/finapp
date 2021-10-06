from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        pagination = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page', self.page.number),
            ('num_pages', self.page.paginator.num_pages),
            ('page_size', self.get_page_size(self.request)),
        ])

        return Response(OrderedDict([
            ('pagination', pagination),
            ('results', data),
        ]))

    def get_paginated_response_schema(self, schema):

        return {
            'type': 'object',
            'properties': {
                'pagination': {
                    'count': {
                        'type': 'integer',
                        'example': 123,
                    },
                    'next': {
                        'type': 'string',
                        'nullable': True,
                    },
                    'previous': {
                        'type': 'string',
                        'nullable': True,
                    },
                    'page': {
                        'type': 'integer',
                        'example': 123,
                    },
                    'num_pages': {
                        'type': 'integer',
                        'example': 123,
                    },
                    'page_size': {
                        'type': 'integer',
                        'example': 123,
                    },
                },
                'results': schema,
            },
        }

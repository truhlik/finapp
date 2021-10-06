from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


path_id_param_int = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, type=openapi.TYPE_INTEGER)]
)

path_group_by_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("group_by", openapi.IN_QUERY, type=openapi.TYPE_STRING)]
)

path_id_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, type=openapi.TYPE_STRING)]
)

path_slug_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("slug", openapi.IN_PATH, type=openapi.TYPE_STRING)]
)

query_q_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("q", openapi.IN_QUERY, type=openapi.TYPE_STRING)]
)

query_rating_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("rating", openapi.IN_QUERY, type=openapi.TYPE_STRING)]
)

query_point_param = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("point", openapi.IN_QUERY, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER))
    ]
)

category_param = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("category_slug", openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ]
)

portfolio_and_category_param = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("portfolio_id", openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter("category_slug", openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ]
)

portfolio_and_category_and_group_by_param = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Filter by portfolio.id"),
        openapi.Parameter("category_id", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Use category.slug for filtering."),
        openapi.Parameter("group_by", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Group by values - use 'category' for dashboard."),
    ],
    serializers=[],
)

portfolio_and_category_and_day_param = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("portfolio_id", openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter("category_slug", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter("days", openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
    ]
)

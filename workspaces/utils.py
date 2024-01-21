from typing import List

from django.http import HttpRequest
from django.db.models import (
    Q,
    QuerySet,
)


def custom_filter(request: HttpRequest, queryset: QuerySet, filter_fields: List):
    # Check if any filter parameters (including empty values) are provided
    if not any(request.query_params.get(field) is not None for field in filter_fields):
        return queryset

    filter_params = {}
    for field in filter_fields:
        filter_params[field] = request.query_params.get(field, None)

    q_objects = Q()
    for field in filter_fields:
        value = filter_params.get(field)
        # Include records where the field is either not None or an empty string
        if value is not None:
            q_objects &= Q(**{field: value})
        
        if value == '':
            continue
    return queryset.filter(q_objects)

from typing import List

from django.http import HttpRequest
from django.db.models import (
    Q,
    QuerySet,
)
from django.core.mail import EmailMessage


def custom_filter(request: HttpRequest, queryset: QuerySet, filter_fields: List):
    filter_params = {}
    for field in filter_fields:
        filter_params[field] = request.query_params.get(field, None)

    if filter_params:
        q_objects = Q()
        for field in filter_fields:
            value = filter_params.get(field)
            if value is not None:
                q_objects &= Q(**{field: value})
        return queryset.filter(q_objects)
    return queryset


def send_email(task_instance):
    subject = 'created task'
    message = f"Task with title '{task_instance.title}' successfully created."
    to_email = 'hamidrezam350000@gmail.com'

    email = EmailMessage(
        subject=subject,
        body=message,
        to=[to_email]
    )
    email.send()

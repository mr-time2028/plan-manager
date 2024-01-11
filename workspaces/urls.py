from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    task_views,
)

router = SimpleRouter()
router.register(r'tasks', task_views.TaskView, basename='tasks')


app_name = "workspaces"
urlpatterns = [
    path('', include(router.urls))
]

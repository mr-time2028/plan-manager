from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    board_views,
    group_views,
    workspace_views,
    task_views,
)

router = SimpleRouter()
router.register(r'workspaces', workspace_views.WorkspaceView, basename='workspaces')
router.register(r'boards', board_views.BoardView, basename='boards')
router.register(r'groups', group_views.GroupView, basename='groups')
router.register(r'tasks', task_views.TaskView, basename='tasks')


app_name = "workspaces"
urlpatterns = [
    path('', include(router.urls))
]

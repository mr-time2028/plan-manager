from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    workspace_view,
    board_view,
)

router = SimpleRouter()
router.register(r'workspaces', workspace_view.WorkspaceView, basename='workspaces')
router.register(r'boards', board_view.BoardView, basename='boards')


app_name = "workspaces"
urlpatterns = [
    path('', include(router.urls))
]

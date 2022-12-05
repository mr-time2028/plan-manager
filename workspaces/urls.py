from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import workspace_view

router = SimpleRouter()
router.register(r'', workspace_view.WorkspaceView, basename='workspaces')


app_name = "workspaces"
urlpatterns = [
    path('', include(router.urls))
]

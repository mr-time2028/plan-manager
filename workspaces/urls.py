from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'', views.WorkspaceView, basename='workspaces')


app_name = "workspaces"
urlpatterns = [
    path('', include(router.urls))
]

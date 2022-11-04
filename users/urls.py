from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
    path('login_web/', views.LoginWebApiView.as_view(), name='login_web'),
    path('login_app/', views.LoginAppApiView.as_view(), name='login_app'),
]

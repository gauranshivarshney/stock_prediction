from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path("register/", views.register_view),
    path("login/", views.login_view),
    path("dashboard/", views.dashboard_view),
]
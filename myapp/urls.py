
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logs/", views.logs_page, name="logs"),

    path("api/state/", views.api_state, name="api_state"),
    path("api/control/", views.api_control, name="api_control"),
    path("api/logs/", views.api_logs, name="api_logs"),
]
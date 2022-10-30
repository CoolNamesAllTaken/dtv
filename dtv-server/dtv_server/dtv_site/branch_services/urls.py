from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_id", views.edit_id, name="create_id"),
    path("edit_id/<str:license_number>", views.edit_id, name="edit_id"),
    path("edit_id/<str:license_number>/<slug:slug>", views.edit_id, name="edit_id_success"),
    path("status/", views.status, name="status"),
    path("get_window_status/", views.get_window_status, name="get_window_status"),
    path("print_id/<str:license_number>", views.print_id),
]
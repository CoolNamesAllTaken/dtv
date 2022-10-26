from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_id", views.create_id, name="create_id"),
    path("edit_id/<str:license_number>", views.edit_id, name="edit_id"),
    path("edit_id/<str:license_number>/<slug:slug>", views.edit_id, name="edit_id_success"),
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_id", views.edit_id, name="create_id"),
    path("edit_id/<str:license_number>", views.edit_id, name="edit_id"),
    path("status/", views.status, name="status"),
    path("get_window_status/", views.get_window_status, name="get_window_status"),
    path("window/<str:window_number>", views.window, name="window"),
    path("get_new_ticket", views.get_new_ticket, name="get_new_ticket"),
    path("get_next_ticket", views.get_next_ticket, name="get_next_ticket"),
    path("create_ticket", views.create_ticket, name="create_ticket"),
    path("complete_ticket", views.complete_ticket, name="complete_ticket"),  
    path("lookup_id", views.lookup_id, name="lookup_id"),
    path("print_id/<str:license_number>", views.print_id),
]
from django.urls import path
from . import views

from django.urls import path
from . import views

app_name = "appointments"   # ✅ add this

urlpatterns = [
    path("book/<int:pet_id>/", views.book_appointment, name="book_appointment"),
    # path("list/", views.appointment_list, name="appointment_list"),
    # path("list/<int:pet_id>/", views.appointment_list, name="appointment_list"),
    path("list/", views.appointment_list, name="appointment_list"),  # optional
    path("reschedule/<int:pk>/", views.reschedule_appointment, name="reschedule_appointment"),
    path("cancel/<int:pk>/", views.cancel_appointment, name="cancel_appointment"),

    path("vet/", views.vet_dashboard, name="vet_dashboard"),
    path("manage/<int:appointment_id>/<str:action>/", views.manage_appointment, name="manage_appointment"),
]

 
 

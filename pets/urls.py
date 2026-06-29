from django.urls import path
from django.shortcuts import redirect
from pets import views
app_name = "pets"


urlpatterns = [
    path('dashboard', views.owner_dashboard, name='owner_dashboard'),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Pet management
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/add/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pet_id>/update-photo/', views.update_pet_photo_ajax, name='update_pet_photo'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path("add-vaccination/", views.add_vaccination, name="add_vaccination"),
    path("add-vaccination/<int:pet_id>/", views.add_vaccination, name="add_vaccination_pet"),
    path("edit-vaccination/<int:pk>/", views.edit_vaccination, name="edit_vaccination"),
    path("delete-vaccination/<int:pk>/", views.delete_vaccination, name="delete_vaccination"),
    # Medical History
    path('pet/<int:pet_id>/history/add/', views.add_medical_record, name='add_medical_record'),
    #new 
    path("history/<int:pk>/edit/", views.edit_medical_history, name="edit_history"),
    path("history/<int:pk>/delete/", views.delete_medical_history, name="delete_history"),

    # Prescriptions
     path("pet/<int:pet_id>/prescription/add/", views.add_prescription, name="add_prescription"),
     
    path("prescription/<int:pk>/edit/", views.edit_prescription, name="edit_prescription"),
    path("prescription/<int:pk>/delete/", views.delete_prescription, name="delete_prescription"),
    # Diet Plan
     path("pets/<int:pet_id>/diet-planner/", views.diet_planner_dashboard, name="diet_planner_dashboard"),
     path("pets/<int:pet_id>/diet/add/", views.add_diet, name="add_diet"),
     path("diet/<int:pk>/edit/", views.edit_diet, name="edit_diet"),
     path("diet/<int:pk>/delete/", views.delete_diet, name="delete_diet"),


    # Allergies
    path("pets/<int:pet_id>/allergies/add/", views.add_allergy, name="add_allergy"),
    path("allergies/<int:pk>/edit/", views.edit_allergy, name="edit_allergy"),
    path("allergies/<int:pk>/delete/", views.delete_allergy, name="delete_allergy"),
    
    #AI 
    path("symptom-checker/", views.symptom_checker, name="symptom_checker"),
    
    # Mood Tracker
    path("pets/<int:pet_id>/mood-tracker/", views.mood_tracker_dashboard, name="mood_tracker_dashboard"),
    path("pets/<int:pet_id>/mood/add/", views.add_mood, name="add_mood"),
    path("mood/<int:pk>/delete/", views.delete_mood, name="delete_mood"),
    
    # Vet Connect
    path("pets/<int:pet_id>/vet-connect/", views.vet_connect_dashboard, name="vet_connect_dashboard"),
    path("pets/<int:pet_id>/vet-connect/request/", views.request_vet_consultation, name="request_vet_consultation"),
    path("pets/<int:pet_id>/vet-connect/report/", views.pet_health_report, name="pet_health_report"),
]

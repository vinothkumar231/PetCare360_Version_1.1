# medical/urls.py
from django.urls import path, include
from .views import MedicalRecordListView, MedicalRecordDetailView, MedicalRecordViewSet
from rest_framework.routers import DefaultRouter

# API router
router = DefaultRouter()
router.register(r"records", MedicalRecordViewSet)

urlpatterns = [
    # Web views
    path("", MedicalRecordListView.as_view(), name="medical_list"),
    path("<int:pk>/", MedicalRecordDetailView.as_view(), name="medical_detail"),

    # API views
    path("api/", include(router.urls)),
]

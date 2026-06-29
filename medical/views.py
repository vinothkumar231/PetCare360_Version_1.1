# medical/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import MedicalRecord

# --------------------------
# Server-rendered views
# --------------------------
class MedicalRecordListView(ListView):
    model = MedicalRecord
    template_name = "medical/record_list.html"
    context_object_name = "records"


class MedicalRecordDetailView(DetailView):
    model = MedicalRecord
    template_name = "medical/record_detail.html"
    context_object_name = "record"

# --------------------------
# Optional API (REST Framework)
# --------------------------
from rest_framework import viewsets
from .serializers import MedicalRecordSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

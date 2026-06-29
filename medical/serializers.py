# medical/serializers.py
from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ["id", "pet", "record_type", "condition", "text", "created_at", "vet"]

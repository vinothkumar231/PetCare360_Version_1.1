from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet

class MedicalRecord(models.Model):
    RECORD_TYPES = [
        ("symptom","Symptom"),
        ("diagnosis","Diagnosis"),
        ("treatment","Treatment"),
        ("note","Note"),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="records")
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    condition = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vet = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet.name} - {self.record_type} - {self.condition or 'n/a'}"


# Create your models here.

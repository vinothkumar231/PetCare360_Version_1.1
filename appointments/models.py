from django.db import models
from django.conf import settings
from pets.models import Pet

User = settings.AUTH_USER_MODEL

class Appointment(models.Model):
    APPOINTMENT_TYPE = [
        ('vet', 'Vet Visit'),
        ('grooming', 'Grooming'),
        ('vaccination', 'Vaccination Camp'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments",default=1) 
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE)
    vet = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="vet_appointments")
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    # Vet-only fields
    prescription = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return f"{self.pet.name} - {self.get_appointment_type_display()} ({self.owner})"

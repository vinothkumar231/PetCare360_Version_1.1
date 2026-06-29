from django.db import models
from django.utils import timezone
from pets.models import Pet

class PetLocation(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.pet.name} at {self.latitude}, {self.longitude} ({self.timestamp})"


class Geofence(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='geofences')
    name = models.CharField(max_length=120, default="Home")
    center_latitude = models.FloatField()
    center_longitude = models.FloatField()
    radius_meters = models.IntegerField(default=100) # e.g. 100 meters
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pet.name} - {self.name} ({self.radius_meters}m radius)"


class LocationAlert(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='location_alerts')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Alert for {self.pet.name}: {self.message}"

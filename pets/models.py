from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import date
from datetime import timedelta
User = get_user_model()

class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('Fish', 'fish'),('Hen', 'Hen'),('Cow', 'Cow'),('other', 'Other')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=80)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='dog')
    breed = models.CharField(max_length=120, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    age_years = models.PositiveIntegerField(blank=True, null=True, editable=False)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
     
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.breed or self.species})"

    def get_absolute_url(self):
        return reverse('pets:pet_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        """Auto-calculate age from birth_date."""
        if self.birth_date:
            today = date.today()
            age_calc = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            self.age_years = max(0, age_calc)
        super().save(*args, **kwargs)

class Vaccination(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=120)
    date_administered = models.DateField()
    next_due = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if self.date_administered and not self.next_due:
            # Auto calculate 1 year later
            self.next_due = self.date_administered + timedelta(days=365)
        super().save(*args, **kwargs)

     
    def __str__(self):
        return f"{self.vaccine_name} - {self.pet.name} ({self.date_administered})"

class MedicalHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="medical_history")
    condition = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_diagnosed = models.DateField()
    treatment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.name} - {self.condition}"


class Prescription(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="prescriptions")
    medicine_name = models.CharField(max_length=120)
    dosage = models.CharField(max_length=120)
    prescribed_on = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicine_name} for {self.pet.name}"

 
class DietPlan(models.Model):
    FOOD_TYPE_CHOICES = [
        ('Dry', 'Dry Food'),
        ('Wet', 'Wet Food'),
        ('Homemade', 'Homemade'),
        ('Raw', 'Raw Food'),
        ('Treats', 'Treats'),
        ('Other', 'Other')
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="diet_plans")
    food_type = models.CharField(max_length=50, choices=FOOD_TYPE_CHOICES, default='Dry')
    food_item = models.CharField(max_length=150)
    quantity = models.CharField(max_length=50, help_text="e.g., 200g, 1 cup")
    time_of_day = models.CharField(
        max_length=50,
        choices=[("Morning", "Morning"), ("Afternoon", "Afternoon"), ("Evening", "Evening"), ("Night", "Night")]
    )
    meal_date = models.DateField(default=timezone.now, help_text="Date of the meal")
    notes = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.food_item} ({self.time_of_day}) on {self.meal_date}"


class Allergy(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="allergies")
    allergen = models.CharField(max_length=150)
    reaction = models.TextField(blank=True)
    severity = models.CharField(
        max_length=50,
        choices=[("Mild", "Mild"), ("Moderate", "Moderate"), ("Severe", "Severe")]
    )

    def __str__(self):
        return f"{self.pet.name} - Allergy: {self.allergen}"


class MoodLog(models.Model):
    MOOD_CHOICES = [
        ('Happy', 'Happy 😄'),
        ('Calm', 'Calm 🙂'),
        ('Anxious', 'Anxious 😟'),
        ('Aggressive', 'Aggressive 😠'),
        ('Low_Energetic', 'Low/Energetic 😴⚡')
    ]
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="mood_logs")
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    log_date = models.DateField(default=timezone.now, help_text="Date of the mood")
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.get_mood_display()} on {self.log_date}"

class VetConsultation(models.Model):
    CONSULTATION_TYPES = [
        ('Normal', 'Normal Consultation'),
        ('Emergency', 'Emergency 🚨')
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending Connection'),
        ('Active', 'Active Consultation'),
        ('Completed', 'Completed')
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vet_consultations")
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPES, default='Normal')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    doctor_notes = models.TextField(blank=True, null=True, help_text="Notes provided by the vet after consult")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.consultation_type} [{self.status}]"
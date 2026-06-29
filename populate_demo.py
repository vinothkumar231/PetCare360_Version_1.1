import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petcare360.settings')
django.setup()

from pets.models import Pet, Vaccination, MedicalHistory, Prescription, DietPlan, Allergy, MoodLog, VetConsultation
from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()
if not users.exists():
    print("No users found. Please create a user first via the UI.")
    exit()

pets = Pet.objects.all()
if not pets.exists():
    print("No pets found. Creating a dummy pet.")
    user = users.first()
    pet = Pet.objects.create(
        name="Golden Boy", 
        species="Dog", 
        breed="Golden Retriever", 
        age_years=3, 
        weight_kg=30.0, 
        owner=user, 
        gender="Male"
    )
    pets = [pet]

today = timezone.now().date()

for pet in pets:
    print(f"Populating data for pet: {pet.name}")
    
    # Vaccinations
    if pet.vaccinations.count() < 2:
        Vaccination.objects.create(pet=pet, vaccine_name="Rabies", date_administered=today - timedelta(days=365), next_due=today + timedelta(days=5), notes="Annual booster required soon.")
        Vaccination.objects.create(pet=pet, vaccine_name="Parvovirus", date_administered=today - timedelta(days=180), next_due=today + timedelta(days=180), notes="Standard vaccine.")

    # Medical History
    if pet.medical_history.count() < 2:
        MedicalHistory.objects.create(pet=pet, condition="Minor Paw Infection", date_diagnosed=today - timedelta(days=45), treatment="Antibiotic ointment", description="Healed well.")
        MedicalHistory.objects.create(pet=pet, condition="Ear Mites", date_diagnosed=today - timedelta(days=120), treatment="Ear drops", description="Cleared up after 2 weeks.")

    # Prescriptions
    if pet.prescriptions.count() < 1:
        Prescription.objects.create(pet=pet, medicine_name="NexGard Spectra", dosage="1 chew/month", prescribed_on=today - timedelta(days=10), notes="Flea and tick prevention.")

    # Diet Plans
    if pet.diet_plans.count() < 2:
        DietPlan.objects.create(pet=pet, food_type="Dry", food_item="Royal Canin Golden Retriever Adult", quantity="200g", meal_date=today, time_of_day="Morning")
        DietPlan.objects.create(pet=pet, food_type="Wet", food_item="Chicken and Vegetables", quantity="150g", meal_date=today, time_of_day="Evening")

    # Allergies
    if pet.allergies.count() < 2:
        Allergy.objects.create(pet=pet, allergen="Chicken Protein", severity="Mild", reaction="Itchy skin, mild scratching.")
        Allergy.objects.create(pet=pet, allergen="Pollen", severity="Moderate", reaction="Sneezing during spring.")

    # Moods
    if pet.mood_logs.count() < 3:
        MoodLog.objects.create(pet=pet, mood="Happy", log_date=today, notes="Played a lot in the park today!")
        MoodLog.objects.create(pet=pet, mood="Calm", log_date=today - timedelta(days=1), notes="Slept through the afternoon.")
        MoodLog.objects.create(pet=pet, mood="Anxious", log_date=today - timedelta(days=2), notes="Loud noises outside.")

print("Demo data successfully populated! All tabs should now have rich sample content.")

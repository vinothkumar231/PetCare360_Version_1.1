import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petcare360.settings')
django.setup()

from pets.models import Pet, Vaccination, MedicalHistory, Prescription, DietPlan, Allergy, MoodLog, VetConsultation
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()
users = User.objects.all()

demo_username = os.environ.get('DEMO_USERNAME', 'demo')
demo_email = os.environ.get('DEMO_EMAIL', 'demo@example.com')
demo_password = os.environ.get('DEMO_PASSWORD') or secrets.token_urlsafe(12)

if not users.exists():
    print(f"No users found. Creating demo user '{demo_username}'.")
    print(f"Demo credentials -> username: {demo_username}, password: {demo_password}")
    user = User.objects.create_user(username=demo_username, email=demo_email, password=demo_password)
else:
    user = users.first()

pets = Pet.objects.filter(owner=user)
if not pets.exists():
    print("No pets found for demo user. Creating a sample pet.")
    pet = Pet.objects.create(
        name="Golden Boy",
        species="Dog",
        breed="Golden Retriever",
        age_years=3,
        weight_kg=30.0,
        owner=user,
        notes="A friendly golden retriever who loves park walks.",
    )
    pets = [pet]
else:
    pets = list(pets)

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

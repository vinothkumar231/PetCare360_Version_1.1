"""
WSGI config for petcare360 project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petcare360.settings")
django.setup()

# Run migrations and seed data automatically on Vercel startup
if os.environ.get("VERCEL"):
    from django.core.management import call_command
    try:
        print("Vercel startup: Running migrations...")
        call_command("migrate", interactive=False)
        
        # Check if the superuser 'vinoth' exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="vinoth").exists():
            print("Vercel startup: Seeding default user 'vinoth'...")
            User.objects.create_superuser("vinoth", "vinoth@example.com", "vinoth@123")
            
            # Seed the database with initial demo data
            from pets.models import Pet, Vaccination, MedicalHistory, Prescription, DietPlan, Allergy, MoodLog
            from datetime import timedelta
            from django.utils import timezone
            
            today = timezone.now().date()
            user = User.objects.get(username="vinoth")
            pet = Pet.objects.create(
                name="Golden Boy", 
                species="Dog", 
                breed="Golden Retriever", 
                age_years=3, 
                weight_kg=30.0, 
                owner=user, 
                gender="Male"
            )
            
            # Vaccinations
            Vaccination.objects.create(pet=pet, vaccine_name="Rabies", date_administered=today - timedelta(days=365), next_due=today + timedelta(days=5), notes="Annual booster required soon.")
            Vaccination.objects.create(pet=pet, vaccine_name="Parvovirus", date_administered=today - timedelta(days=180), next_due=today + timedelta(days=180), notes="Standard vaccine.")
            
            # Medical History
            MedicalHistory.objects.create(pet=pet, condition="Minor Paw Infection", date_diagnosed=today - timedelta(days=45), treatment="Antibiotic ointment", description="Healed well.")
            MedicalHistory.objects.create(pet=pet, condition="Ear Mites", date_diagnosed=today - timedelta(days=120), treatment="Ear drops", description="Cleared up after 2 weeks.")
            
            # Prescriptions
            Prescription.objects.create(pet=pet, medicine_name="NexGard Spectra", dosage="1 chew/month", prescribed_on=today - timedelta(days=10), notes="Flea and tick prevention.")
            
            # Diet Plans
            DietPlan.objects.create(pet=pet, food_type="Dry", food_item="Royal Canin Golden Retriever Adult", quantity="200g", meal_date=today, time_of_day="Morning")
            DietPlan.objects.create(pet=pet, food_type="Wet", food_item="Chicken and Vegetables", quantity="150g", meal_date=today, time_of_day="Evening")
            
            # Allergies
            Allergy.objects.create(pet=pet, allergen="Chicken Protein", severity="Mild", reaction="Itchy skin, mild scratching.")
            Allergy.objects.create(pet=pet, allergen="Pollen", severity="Moderate", reaction="Sneezing during spring.")
            
            # Moods
            MoodLog.objects.create(pet=pet, mood="Happy", log_date=today, notes="Played a lot in the park today!")
            MoodLog.objects.create(pet=pet, mood="Calm", log_date=today - timedelta(days=1), notes="Slept through the afternoon.")
            MoodLog.objects.create(pet=pet, mood="Anxious", log_date=today - timedelta(days=2), notes="Loud noises outside.")
            print("Vercel startup: Database seeding completed.")
    except Exception as e:
        print("Vercel startup: Error during auto-migration/seeding:", e)

application = get_wsgi_application()
app = application

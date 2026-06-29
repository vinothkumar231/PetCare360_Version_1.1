import os
import django
import random
from datetime import timedelta, datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petcare360.settings')
django.setup()

from pets.models import Pet, MoodLog, DietPlan, Vaccination, MedicalHistory
from appointments.models import Appointment
from trackers.models import PetLocation
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
        species="dog", 
        breed="Golden Retriever", 
        birth_date=timezone.now().date() - timedelta(days=1000),
        weight_kg=30.0, 
        owner=user, 
    )
    pets = [pet]

today = timezone.now().date()
now = timezone.now()

mood_choices = ['Happy', 'Calm', 'Anxious', 'Low_Energetic']
food_items = [
    ("Royal Canin", "Dry"),
    ("Pedigree", "Dry"),
    ("Chicken Rice", "Homemade"),
    ("Salmon chunks", "Wet")
]

print("Starting population of historical data for the last 7 days...")

for pet in pets:
    print(f"Adding data for {pet.name}...")
    
    for i in range(8):  # Last 7 days + today
        log_date = today - timedelta(days=i)
        
        # 1. Mood Logs
        # Add 1 mood record per day
        if not MoodLog.objects.filter(pet=pet, log_date=log_date).exists():
            mood = random.choice(mood_choices)
            notes = f"Auto-generated log for {log_date}. {pet.name} was feeling {mood}."
            MoodLog.objects.create(pet=pet, mood=mood, log_date=log_date, notes=notes)
        
        # 2. Diet Plans
        # Add 2 meals per day
        for tod in ["Morning", "Evening"]:
            if not DietPlan.objects.filter(pet=pet, meal_date=log_date, time_of_day=tod).exists():
                item, ftype = random.choice(food_items)
                qty = f"{random.randint(100, 300)}g"
                DietPlan.objects.create(
                    pet=pet, 
                    food_type=ftype, 
                    food_item=item, 
                    quantity=qty, 
                    time_of_day=tod, 
                    meal_date=log_date
                )
        
        # 3. Appointments
        # Add a completed appointment in the past
        if i in [2, 5]: # 2 and 5 days ago
            if not Appointment.objects.filter(pet=pet, date=log_date).exists():
                Appointment.objects.create(
                    owner=pet.owner,
                    pet=pet,
                    appointment_type=random.choice(['vet', 'grooming']),
                    date=log_date,
                    time=datetime.strptime(f"{random.randint(9, 17)}:00", "%H:%M").time(),
                    notes=f"Past visit for routine checkup on {log_date}",
                    status='completed'
                )

    # 4. Location History (last 24 hours, hourly)
    print(f"Adding location history for {pet.name}...")
    base_lat = 40.7128 # NYC base
    base_lon = -74.0060
    for h in range(24):
        timestamp = now - timedelta(hours=h)
        # Adding slight variations
        lat = base_lat + (random.random() - 0.5) * 0.01
        lon = base_lon + (random.random() - 0.5) * 0.01
        PetLocation.objects.create(
            pet=pet,
            latitude=lat,
            longitude=lon,
            timestamp=timestamp
        )

    # 5. Future Appointments
    # Add some pending appointments for next week
    for j in range(1, 4):
        future_date = today + timedelta(days=j)
        if not Appointment.objects.filter(pet=pet, date=future_date).exists():
            Appointment.objects.create(
                owner=pet.owner,
                pet=pet,
                appointment_type='vet',
                date=future_date,
                time=datetime.strptime(f"{random.randint(9, 17)}:00", "%H:%M").time(),
                notes=f"Upcoming vaccination camp on {future_date}",
                status='pending'
            )

print("Data population complete!")

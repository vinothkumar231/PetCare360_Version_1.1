from django.utils import timezone
from datetime import timedelta

def generate_smart_summary(pet):
    """
    Analyzes the last 7 days of Diet, Mood, and Medical logs to 
    generate quick bullet points for the vet.
    """
    summary = []
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)

    # Mood Check
    recent_moods = pet.mood_logs.filter(log_date__gte=seven_days_ago)
    anxious_count = recent_moods.filter(mood__in=['Anxious', 'Aggressive']).count()
    low_count = recent_moods.filter(mood='Low_Energetic').count()
    
    if anxious_count >= 2:
        summary.append(f"⚠️ High anxiety/stress levels noted ({anxious_count} incidents in last 7 days).")
    if low_count >= 3:
        summary.append(f"⚠️ Unusually low energy or lethargy for {low_count} of the last 7 days.")
        
    # Diet Check
    recent_diets = pet.diet_plans.filter(meal_date__gte=seven_days_ago)
    if recent_diets.exists() and recent_diets.count() < 10:  # Assuming avg 2 meals/day
        summary.append("⚠️ Potentially skipped meals: Intake frequency is lower than usual this week.")

    # Medical History Check
    recent_medical = pet.medical_history.filter(date_diagnosed__gte=today - timedelta(days=30))
    if recent_medical.exists():
        conds = ", ".join([m.condition for m in recent_medical])
        summary.append(f"🩺 Recent medical issues in last 30 days: {conds}.")

    if not summary:
        summary.append("✅ No significant negative trends detected in the last 7 days.")

    return summary

def get_nearby_vets():
    """
    Returns a mocked list of nearby veterinary clinics.
    """
    return [
        {
            "name": "City Paws Animal Hospital",
            "distance": "1.2 km away",
            "address": "421 Veterinary Ave, Downtown",
            "phone": "+1 (555) 123-4567",
            "status": "Open 24/7",
            "rating": "4.8"
        },
        {
            "name": "Evergreen Vet Clinic",
            "distance": "3.5 km away",
            "address": "88 Pine Street, Suburbs",
            "phone": "+1 (555) 987-6543",
            "status": "Closes at 8 PM",
            "rating": "4.6"
        },
        {
            "name": "Rapid Response Pet ER",
            "distance": "5.0 km away",
            "address": "911 Urgent Care Blvd, Uptown",
            "phone": "+1 (800) 999-EMERG",
            "status": "Open 24/7",
            "rating": "4.9"
        }
    ]

def compile_full_health_report(pet):
    """
    Aggregates all of the pet's core health data into a single structured object.
    """
    today = timezone.now().date()
    
    return {
        "pet_profile": {
            "name": pet.name,
            "breed": pet.breed,
            "age": pet.age_years,
            "weight": pet.weight_kg,
            "gender": getattr(pet, 'gender', 'Unknown')
        },
        "vaccinations": pet.vaccinations.order_by('-date_administered')[:10],
        "medical_history": pet.medical_history.order_by('-date_diagnosed')[:10],
        "allergies": pet.allergies.all(),
        "recent_diet": pet.diet_plans.order_by('-meal_date')[:14],
        "recent_mood": pet.mood_logs.order_by('-log_date')[:7]
    }

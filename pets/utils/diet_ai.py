from django.utils import timezone
from datetime import timedelta

def get_diet_health_status(pet):
    """
    Returns the diet health status of the pet:
    - Balanced ✅
    - Needs Improvement ⚠️
    - Poor 🚨
    
    Logic based on logged meals over the last 7 days.
    """
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)
    
    # Get recent diet plans
    recent_diets = pet.diet_plans.filter(meal_date__gte=seven_days_ago, meal_date__lte=today)
    meal_count = recent_diets.count()
    
    if meal_count >= 14:  # At least 2 meals a day for 7 days
        return {
            'status_text': 'Balanced Diet',
            'icon': '✅',
            'color': 'success',
            'message': 'Keep it up! Your pet is maintaining a consistent feeding schedule.'
        }
    elif meal_count >= 7:  # At least 1 meal a day
        return {
            'status_text': 'Needs Improvement',
            'icon': '⚠️',
            'color': 'warning',
            'message': 'Try to maintain a more consistent 2-3 meals per day schedule.'
        }
    else:
        return {
            'status_text': 'Poor Diet Tracking',
            'icon': '🚨',
            'color': 'danger',
            'message': 'Very few meals tracked recently. Ensuring a proper diet is crucial!'
        }

def get_smart_suggestions(pet):
    """
    Returns a list of smart text suggestions based on pet attributes.
    """
    suggestions = []
    
    # Basic Age & Weight mock logic
    if pet.age_years is not None:
        if pet.age_years < 1:
            suggestions.append("Kitten/Puppy phase: Ensure high protein and frequent, smaller meals (3-4 times/day).")
        elif pet.age_years >= 7:
            suggestions.append("Senior Pet: Consider foods with joint support (omega-3, glucosamine) and lower calories.")
    
    if pet.weight_kg is not None:
        if pet.weight_kg > 20:
            suggestions.append(f"Large breed/weight ({pet.weight_kg}kg): Monitor portion sizes carefully to avoid obesity and joint stress.")
        elif pet.weight_kg < 5:
            suggestions.append("Small breed/weight: Consider bite-sized kibble and highly digestible ingredients.")
            
    # Default tips if not enough data
    if len(suggestions) < 2:
        suggestions.append("Ensure constant access to fresh, clean water.")
        suggestions.append("Mix wet food occasionally to keep them hydrated and excited about meals.")
        
    return suggestions

def get_alerts(pet):
    """
    Returns alerts specifically for today.
    """
    alerts = []
    today = timezone.now().date()
    todays_meals = pet.diet_plans.filter(meal_date=today)
    times_logged = [m.time_of_day for m in todays_meals]
    
    if len(todays_meals) > 4:
        alerts.append("Overfeeding Detected: Your pet has received more than 4 meals today!")
        
    # Example skipped meal logic:
    # If it's afternoon and no morning meal is logged
    hour = timezone.now().hour
    if hour >= 12 and 'Morning' not in times_logged:
        alerts.append("Skipped Meal: Morning meal hasn't been logged today.")
    if hour >= 18 and 'Afternoon' not in times_logged:
        alerts.append("Skipped Meal: Afternoon meal hasn't been logged today.")
        
    return alerts

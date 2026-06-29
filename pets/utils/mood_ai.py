from django.utils import timezone
from datetime import timedelta

def get_mood_analytics(pet):
    """
    Returns the mood health status of the pet:
    - Emotionally Healthy ✅
    - Mild Stress ⚠️
    - Needs Attention 🚨
    
    Logic based on logged moods over the last 14 days.
    """
    today = timezone.now().date()
    fourteen_days_ago = today - timedelta(days=14)
    recent_moods = pet.mood_logs.filter(log_date__gte=fourteen_days_ago, log_date__lte=today)
    
    if not recent_moods.exists():
        return {
            'status_text': 'No Data',
            'icon': '😶',
            'color': 'secondary',
            'message': 'Start logging your pet\'s daily mood to get insights.'
        }
        
    negative_moods = recent_moods.filter(mood__in=['Anxious', 'Aggressive'])
    negative_rate = negative_moods.count() / recent_moods.count()

    if negative_rate >= 0.3:  # 30% or more negative
        return {
            'status_text': 'Needs Attention',
            'icon': '🚨',
            'color': 'danger',
            'message': 'Your pet has been frequently anxious or aggressive recently. Please observe their environment.'
        }
    elif negative_rate >= 0.1:  # between 10% and 30%
        return {
            'status_text': 'Mild Stress',
            'icon': '⚠️',
            'color': 'warning',
            'message': 'Your pet shows occasional signs of stress. A little extra comfort might help!'
        }
    else:
        return {
            'status_text': 'Emotionally Healthy',
            'icon': '✅',
            'color': 'success',
            'message': 'Your pet is displaying a stable, happy, and calm emotional state!'
        }

def get_mood_suggestions(pet):
    """
    Returns a list of specific engagement ideas/tips.
    """
    import random
    
    all_tips = [
        "Increase active playtime by 15 minutes today.",
        "Take them for an exploring sniff-walk to stimulate their brain.",
        "Avoid loud environments or chaotic areas for the next 24 hours.",
        "Spend 10 minutes doing basic command training with high-value treats.",
        "Introduce a new puzzle toy or lick-mat for mental enrichment."
    ]
    
    # We could base this explicitly on recent moods but randomization works well as a start
    return random.sample(all_tips, 3)

def get_mood_alerts(pet):
    """
    Checks for sudden, acute negative streaks.
    """
    alerts = []
    today = timezone.now().date()
    three_days_ago = today - timedelta(days=3)
    
    recent = pet.mood_logs.filter(log_date__gte=three_days_ago, log_date__lte=today).order_by('-log_date')
    
    aggression_count = sum(1 for m in recent if m.mood == 'Aggressive')
    anxiety_count = sum(1 for m in recent if m.mood == 'Anxious')
    low_count = sum(1 for m in recent if m.mood == 'Low_Energetic')
    
    if aggression_count >= 2:
        alerts.append("Sudden Aggression: We noticed multiple aggressive moods over the last 3 days.")
    if anxiety_count >= 2:
        alerts.append("Frequent Anxiety: Your pet has been very anxious recently. Check for new stressors.")
    if low_count >= 3:
        alerts.append("Low Energy Streak: Low mood for multiple days. Ensure they are feeling well physically.")
        
    return alerts

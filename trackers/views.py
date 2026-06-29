from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from pets.models import Pet

@login_required
def tracker_dashboard(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    return render(request, 'trackers/tracker_dashboard.html', {'pet': pet})

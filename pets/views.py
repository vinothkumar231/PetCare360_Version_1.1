from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Pet
from .forms import PetForm, VaccinationForm 
from django.contrib import messages
from .forms import SignupForm, ForgotPasswordForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden

from django.utils import timezone
from django.db.models import Count,Avg
from .models import Pet, Vaccination
from datetime import date
 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet, Vaccination, MedicalHistory, Prescription, DietPlan, Allergy
from .forms import VaccinationForm, MedicalHistoryForm, PrescriptionForm, DietPlanForm, AllergyForm
from appointments.models import Appointment


def csrf_failure(request, reason=""):
    is_ajax = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest" or request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax:
        return JsonResponse({'success': False, 'message': 'CSRF verification failed. Please refresh and try again.'}, status=403)
    return HttpResponseForbidden('CSRF verification failed. Request aborted.')

from .forms import PrescriptionForm,DietPlanForm,AllergyForm,MedicalHistoryForm
import joblib
import os
import pickle
from django.conf import settings
from django.shortcuts import render
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

@login_required
def owner_dashboard(request):
    owner = request.user
    pets = Pet.objects.filter(owner=request.user)
    
    # Stats
    total_pets = pets.count()
    avg_age = pets.aggregate(Avg('age_years'))['age_years__avg'] or 0
    total_vaccinations = Vaccination.objects.filter(pet__owner=owner).count()  
    # Vaccinations due soon (within 30 days)
    today = timezone.now().date()
    due_soon = Vaccination.objects.filter(
        pet__owner=owner,
        next_due__isnull=False,
        next_due__gte=today,
        next_due__lte=today + timezone.timedelta(days=30)
    ).order_by('next_due')[:5]
    # fetch upcoming vaccinations
    reminders = []
    for pet in pets:
        last_vacc = pet.vaccinations.order_by('-date_administered').first()
        if last_vacc and last_vacc.next_due:
            days_left = (last_vacc.next_due - date.today()).days
            reminders.append({
                "pet": pet,
                "vaccine": last_vacc.vaccine_name,
                "next_date": last_vacc.next_due,
                "days_left": days_left,
                "is_overdue": days_left < 0,  # flag
                "abs_days": abs(days_left),   # precomputed abs
            })
    # Fetch appointments
    appointments = Appointment.objects.filter(owner=owner).order_by('date', 'time')
    upcoming_appointments = appointments.count()

    context = {
        'owner': owner,
        'pets': pets,
        'total_pets': total_pets,
        'avg_age': round(avg_age, 1),
        'total_vaccinations': total_vaccinations,
        'due_soon': due_soon,
        "reminders": reminders,
        'appointments': appointments,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'pets/owner_dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        if user:
            login(request, user)
            if is_ajax:
                from django.urls import reverse
                return JsonResponse({'success': True, 'redirect_url': reverse('pets:owner_dashboard')})
            return redirect("pets:owner_dashboard")

        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=401)
            messages.error(request, "Invalid username or password")
            return render(request, 'auth/login.html', status=401)
    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        confirm = request.POST['password2']
        if password != confirm:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("pets:owner_dashboard")

    return render(request, 'auth/signup.html')

def logout_view(request):
    logout(request)
    return redirect("pets:login")

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.success(request, 'Password reset link sent (demo only).')
            else:
                messages.error(request, 'Email not found')
    else:
        form = ForgotPasswordForm()
    return render(request, 'auth/forgot_password.html', {'form': form})

@login_required
def pet_list(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/pet_list.html', {'pets': pets})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    vaccinations = pet.vaccinations.all()
    return render(request, 'pets/pet_detail.html', {'pet': pet, 'vaccinations': vaccinations})

@login_required
def pet_create(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)  # 👈 request.FILES is needed
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            # Seed basic starter data for newly created pets
            today = timezone.now().date()
            if not pet.vaccinations.exists():
                Vaccination.objects.create(
                    pet=pet,
                    vaccine_name="Initial Wellness Check",
                    date_administered=today,
                    next_due=today + timezone.timedelta(days=365),
                    notes="Initial health profile created automatically."
                )
            if not pet.medical_history.exists():
                MedicalHistory.objects.create(
                    pet=pet,
                    condition="Profile created",
                    date_diagnosed=today,
                    treatment="Initial check-up",
                    description="Basic profile data seeded for the new pet."
                )
            if not pet.prescriptions.exists():
                Prescription.objects.create(
                    pet=pet,
                    medicine_name="General Wellness",
                    dosage="As needed",
                    prescribed_on=today,
                    notes="Starter prescription record for pet profile."
                )
            if not pet.diet_plans.exists():
                DietPlan.objects.create(
                    pet=pet,
                    food_type="Dry",
                    food_item="Starter nutrition plan",
                    quantity="200g",
                    meal_date=today,
                    time_of_day="Morning",
                    notes="Basic diet plan added automatically."
                )
            if not pet.allergies.exists():
                Allergy.objects.create(
                    pet=pet,
                    allergen="None",
                    severity="Mild",
                    reaction="No known allergies recorded yet."
                )
            if not pet.mood_logs.exists():
                MoodLog.objects.create(
                    pet=pet,
                    mood="Happy",
                    log_date=today,
                    notes="New pet profile created."
                )

            messages.success(request, "Pet created successfully. Starter profile data has been added.")
            return redirect("pets:pet_list")
    else:
        form = PetForm()
    return render(request, "pets/add_pet.html", {"form": form})

@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/pet_form.html', {'form': form})

@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        return redirect('pets:pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})

@login_required
def add_vaccination(request, pet_id=None):
    if pet_id:
        pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    else:
        pet = None
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            # ensure vaccination belongs to logged-in user’s pet
            if vaccination.pet.owner == request.user:
                vaccination.save()
            return redirect('pets:owner_dashboard')
    else:
        # if pet is passed, pre-fill the pet field
        form = VaccinationForm(initial={'pet': pet}) if pet else VaccinationForm()
    return render(request, "pets/add_vaccination.html", {"form": form})

@login_required
def edit_vaccination(request, pk):
    vaccination = get_object_or_404(Vaccination, pk=pk, pet__owner=request.user)
    if request.method == "POST":
        form = VaccinationForm(request.POST, instance=vaccination)
        if form.is_valid():
            form.save()
            return redirect('pets:owner_dashboard')
    else:
        form = VaccinationForm(instance=vaccination)
    return render(request, "pets/edit_vaccination.html", {"form": form})


# DELETE VACCINATION
@login_required
def delete_vaccination(request, pk):
    vaccination = get_object_or_404(Vaccination, id=pk, pet__owner=request.user)
    pet_id = vaccination.pet.id
    if request.method == "POST":
        vaccination.delete()
        return redirect("pets:pet_detail", pk=pet_id)
    return render(request, "pets/confirm_delete.html", {"object": vaccination, "type": "Vaccination"})


# ADD
@login_required
def add_prescription(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.pet = pet
            prescription.save()
            return redirect("pets:pet_detail", pk=pet.id)
    else:
        form = PrescriptionForm()
    return render(request, "pets/prescription_form.html", {"form": form, "pet": pet})

# EDIT
@login_required
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, id=pk, pet__owner=request.user)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect("pets:pet_detail", pk=prescription.pet.id)
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, "pets/prescription_form.html", {"form": form, "pet": prescription.pet})

# DELETE
@login_required
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, id=pk, pet__owner=request.user)
    pet_id = prescription.pet.id
    if request.method == "POST":
        prescription.delete()
        return redirect("pets:pet_detail", pk=pet_id)
    return render(request, "pets/confirm_delete.html", {"object": prescription, "type": "Prescription"})


# -------- DIET PLAN --------
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, DietPlan
from .forms import DietPlanForm
from .utils.diet_ai import get_diet_health_status, get_smart_suggestions, get_alerts
import json

@login_required
def diet_planner_dashboard(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    diet_plans = pet.diet_plans.all().order_by('-meal_date', '-created_on')
    
    # Get AI insights
    health_status = get_diet_health_status(pet)
    suggestions = get_smart_suggestions(pet)
    alerts = get_alerts(pet)
    
    # Chart Data (last 7 days counts)
    import datetime
    from django.utils import timezone
    today = timezone.now().date()
    labels = [(today - datetime.timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
    data = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        count = pet.diet_plans.filter(meal_date=d).count()
        data.append(count)
        
    context = {
        'pet': pet,
        'diet_plans': diet_plans,
        'health_status': health_status,
        'suggestions': suggestions,
        'alerts': alerts,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data)
    }
    return render(request, "pets/diet_planner_dashboard.html", context)

# ADD
@login_required
def add_diet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == "POST":
        form = DietPlanForm(request.POST)
        if form.is_valid():
            diet = form.save(commit=False)
            diet.pet = pet
            diet.save()
            return redirect("pets:diet_planner_dashboard", pet_id=pet.id)
    else:
        form = DietPlanForm()
    return render(request, "pets/diet_form.html", {"form": form, "pet": pet})

# EDIT
@login_required
def edit_diet(request, pk):
    diet = get_object_or_404(DietPlan, id=pk, pet__owner=request.user)
    if request.method == "POST":
        form = DietPlanForm(request.POST, instance=diet)
        if form.is_valid():
            form.save()
            return redirect("pets:diet_planner_dashboard", pet_id=diet.pet.id)
    else:
        form = DietPlanForm(instance=diet)
    return render(request, "pets/diet_form.html", {"form": form, "pet": diet.pet})

# DELETE
@login_required
def delete_diet(request, pk):
    diet = get_object_or_404(DietPlan, id=pk, pet__owner=request.user)
    pet_id = diet.pet.id
    if request.method == "POST":
        diet.delete()
        return redirect("pets:diet_planner_dashboard", pet_id=pet_id)
    return render(request, "pets/diet_confirm_delete.html", {"diet": diet})


# -------- ALLERGIES --------
#correct code
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, Allergy
from .forms import AllergyForm

# ADD
@login_required
def add_allergy(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == "POST":
        form = AllergyForm(request.POST)
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.pet = pet
            allergy.save()
            return redirect("pets:pet_detail", pk=pet.id)
    else:
        form = AllergyForm()
    return render(request, "pets/allergy_form.html", {"form": form, "pet": pet})

# EDIT
@login_required
def edit_allergy(request, pk):
    allergy = get_object_or_404(Allergy, id=pk, pet__owner=request.user)
    if request.method == "POST":
        form = AllergyForm(request.POST, instance=allergy)
        if form.is_valid():
            form.save()
            return redirect("pets:pet_detail", pk=allergy.pet.id)
    else:
        form = AllergyForm(instance=allergy)
    return render(request, "pets/allergy_form.html", {"form": form, "pet": allergy.pet})

# DELETE
@login_required
def delete_allergy(request, pk):
    allergy = get_object_or_404(Allergy, id=pk, pet__owner=request.user)
    pet_id = allergy.pet.id
    if request.method == "POST":
        allergy.delete()
        return redirect("pets:pet_detail", pk=pet_id)
    return render(request, "pets/confirm_delete.html", {"object": allergy, "type": "Allergy"})

# @login_required
# def add_allergy(request, pet_id):
#     pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
#     if request.method == "POST":
#         form = AllergyForm(request.POST)
#         if form.is_valid():
#             a = form.save(commit=False)
#             a.pet = pet
#             a.save()
#     return redirect("pets:owner_dashboard")

# @login_required
# def edit_allergy(request, pk):
#     a = get_object_or_404(Allergy, id=pk, pet__owner=request.user)
#     if request.method == "POST":
#         form = AllergyForm(request.POST, instance=a)
#         if form.is_valid():
#             form.save()
#     return redirect("pets:owner_dashboard")

# @login_required
# def delete_allergy(request, pk):
#     a = get_object_or_404(Allergy, id=pk, pet__owner=request.user)
#     a.delete()
#     return redirect("pets:owner_dashboard")

#medical report (new)
@login_required
def add_medical_record(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

    if request.method == "POST":
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.pet = pet   # link record to the pet
            history.save()
            return redirect('pets:pet_detail', pk=pet.id)
  # 👈 redirect back to pet details page
    else:
        form = MedicalHistoryForm()

    return render(request, 'pets/add_medical_history.html', {
        'form': form,
        'pet': pet
    })

# EDIT
@login_required
def edit_medical_history(request, pk):
    history = get_object_or_404(MedicalHistory, id=pk, pet__owner=request.user)
    if request.method == "POST":
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            return redirect("pets:pet_detail", pk=history.pet.id)
    else:
        form = MedicalHistoryForm(instance=history)
    return render(request, "pets/medical_history_form.html", {"form": form, "pet": history.pet})

# DELETE
@login_required
def delete_medical_history(request, pk):
    history = get_object_or_404(MedicalHistory, id=pk, pet__owner=request.user)
    pet_id = history.pet.id
    if request.method == "POST":
        history.delete()
        return redirect("pets:pet_detail", pk=pet_id)
    return render(request, "pets/confirm_delete.html", {"object": history, "type": "Medical Record"})


# Load vectorizer + matrix once (global)
# vectorizer_path = os.path.join(settings.BASE_DIR, "models", "tfidf_vectorizer.pkl")
# matrix_path = os.path.join(settings.BASE_DIR, "models", "tfidf_matrix.pkl")

# tfidf_vectorizer = joblib.load(vectorizer_path)
# tfidf_matrix = joblib.load(matrix_path)
# @login_required
# def symptom_checker(request):
#     diagnosis = None
#     if request.method == "POST":
#         symptoms = request.POST.get("symptoms")

#         if symptoms:
#             # Transform input text
#             input_vector = tfidf_vectorizer.transform([symptoms])

#             # Compute similarity with dataset
#             from sklearn.metrics.pairwise import cosine_similarity
#             similarity_scores = cosine_similarity(input_vector, tfidf_matrix)

#             # Find most similar case
#             best_match_idx = similarity_scores.argmax()

#             # For now, just show index (later we map to disease name from CSV)
#             diagnosis = f"Possible match with dataset case #{best_match_idx}"
    
#     return render(request, "pets/symptom_checker.html", {"diagnosis": diagnosis})
# vectorizer_path = os.path.join(settings.BASE_DIR, "models", "tfidf_vectorizer.pkl")
# matrix_path = os.path.join(settings.BASE_DIR, "models", "tfidf_matrix.pkl")
# dataset_path = os.path.join(settings.BASE_DIR, "models", "pet-health-symptoms-dataset.csv")

# tfidf_vectorizer = joblib.load(vectorizer_path)
# tfidf_matrix = joblib.load(matrix_path)
# df = pd.read_csv(dataset_path)   # Dataset with Symptoms + Disease (+ maybe Treatment)

# def symptom_checker(request):
#     diagnosis = None
#     treatment = None
#     if request.method == "POST":
#         symptoms = request.POST.get("symptoms")

#         if symptoms:
#             # Vectorize input
#             input_vector = tfidf_vectorizer.transform([symptoms])

#             # Compute cosine similarity
#             similarity_scores = cosine_similarity(input_vector, tfidf_matrix)

#             # Best match row
#             best_match_idx = similarity_scores.argmax()

#             # Fetch disease name
#             diagnosis = df.iloc[best_match_idx]["condition"]


#             # Optional: if dataset has treatment column
#             if "Treatment" in df.columns:
#                 treatment = df.iloc[best_match_idx]["Treatment"]

#     return render(
#         request,
#         "pets/symptom_checker.html",
#         {"diagnosis": diagnosis, "treatment": treatment},
#     )
#new
# Paths
symptom_path = os.path.join(settings.BASE_DIR, "models", "pet-health-symptoms-dataset.csv")
profile_path = os.path.join(settings.BASE_DIR, "models", "pet_dataset_with_profiles.csv")
vectorizer_path = os.path.join(settings.BASE_DIR, "models", "tfidf_vectorizer.pkl")
matrix_path = os.path.join(settings.BASE_DIR, "models", "tfidf_matrix.pkl")

# Load datasets
symptom_df = pd.read_csv(symptom_path)
profile_df = pd.read_csv(profile_path)

# Load AI model objects (✅ real TF-IDF and sparse matrix)
with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

with open(matrix_path, "rb") as f:
    tfidf_matrix = pickle.load(f)


@login_required
def symptom_checker(request):
    result = None

    if request.method == "POST":
        user_input = request.POST.get("symptoms")

        if user_input:
            # Transform input into vector
            user_vec = vectorizer.transform([user_input])
            sims = cosine_similarity(user_vec, tfidf_matrix)

            # Find best match
            best_match_idx = sims.argmax()
            diagnosis = symptom_df.iloc[best_match_idx]["condition"]
            record_type = symptom_df.iloc[best_match_idx]["record_type"]

            # Match with Care Profile dataset
            care_profile = None
            if diagnosis in profile_df["condition"].values:
                care_profile = profile_df.loc[
                    profile_df["condition"] == diagnosis, "Care_Profile"
                ].values[0]

            result = {
                "input": user_input,
                "condition": diagnosis,
                "record_type": record_type,
                "care_profile": care_profile if care_profile else "Not available",
                "match_case": best_match_idx,
            }

    return render(request, "pets/symptom_checker.html", {"result": result})
 
# -------- MOOD TRACKER --------
from .models import MoodLog
from .forms import MoodLogForm
from .utils.mood_ai import get_mood_analytics, get_mood_suggestions, get_mood_alerts
import json
import datetime

@login_required
def mood_tracker_dashboard(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    mood_logs = pet.mood_logs.all().order_by('-log_date', '-created_on')
    
    analytics = get_mood_analytics(pet)
    suggestions = get_mood_suggestions(pet)
    alerts = get_mood_alerts(pet)
    
    # Chart Data (last 7 days mapping mood to a score for line chart)
    today = timezone.now().date()
    labels = [(today - datetime.timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
    data = []
    
    # Simple scoring: Happy=5, Calm=4, Energetic=3, Anxious=2, Aggressive=1
    score_map = {
        'Happy': 5,
        'Calm': 4,
        'Low_Energetic': 3,
        'Anxious': 2,
        'Aggressive': 1
    }
    
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        day_moods = pet.mood_logs.filter(log_date=d)
        if day_moods.exists():
            # average score
            avg = sum(score_map[m.mood] for m in day_moods) / day_moods.count()
            data.append(round(avg, 1))
        else:
            data.append(None) # missing data
            
    context = {
        'pet': pet,
        'mood_logs': mood_logs,
        'analytics': analytics,
        'suggestions': suggestions,
        'alerts': alerts,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data)
    }
    return render(request, "pets/mood_tracker_dashboard.html", context)

@login_required
def add_mood(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == "POST":
        form = MoodLogForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.pet = pet
            mood.save()
            return redirect("pets:mood_tracker_dashboard", pet_id=pet.id)
    else:
        form = MoodLogForm()
    return render(request, "pets/mood_form.html", {"form": form, "pet": pet})

@login_required
def delete_mood(request, pk):
    mood = get_object_or_404(MoodLog, id=pk, pet__owner=request.user)
    pet_id = mood.pet.id
    if request.method == "POST":
        mood.delete()
        return redirect("pets:mood_tracker_dashboard", pet_id=pet_id)
    return render(request, "pets/confirm_delete.html", {"object": mood, "type": "Mood Log"})

# -------- SMART VET CONNECT --------
from .models import VetConsultation
from .utils.vet_connect_ai import generate_smart_summary, get_nearby_vets, compile_full_health_report
from django.contrib import messages

@login_required
def vet_connect_dashboard(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    
    smart_summary = generate_smart_summary(pet)
    nearby_vets = get_nearby_vets()
    active_consultations = pet.vet_consultations.exclude(status='Completed').order_by('-created_at')

    context = {
        'pet': pet,
        'smart_summary': smart_summary,
        'nearby_vets': nearby_vets,
        'active_consultations': active_consultations
    }
    return render(request, "pets/vet_connect_dashboard.html", context)

@login_required
def request_vet_consultation(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    
    if request.method == "POST":
        consult_type = request.POST.get('consultation_type', 'Normal')
        
        # Create pending consult
        consult = VetConsultation.objects.create(
            pet=pet,
            consultation_type=consult_type,
            status='Pending'
        )
        
        if consult_type == 'Emergency':
            messages.error(request, "🚨 EMERGENCY MODE ACTIVATED: Broadcasting pet details to nearest available emergency vets!")
        else:
            messages.success(request, f"Consultation requested! Sharing {pet.name}'s health report with a veterinarian.")
            
    return redirect('pets:vet_connect_dashboard', pet_id=pet.id)

@login_required
def pet_health_report(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    health_data = compile_full_health_report(pet)
    
    context = {
        'pet': pet,
        'report': health_data
    }
    return render(request, "pets/pet_health_report.html", context)

@login_required
def update_pet_photo_ajax(request, pet_id):
    if request.method == "POST":
        pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
        try:
            if 'image' in request.FILES:
                if pet.photo:
                    pet.photo.delete(save=False)
                
                pet.photo = request.FILES['image']
                pet.save()
                
                return JsonResponse({'success': True, 'new_url': pet.photo.url})
            return JsonResponse({'success': False, 'message': 'No image provided'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
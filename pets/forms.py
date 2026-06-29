from django import forms
from .models import Pet, Vaccination,Prescription, MedicalHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DietPlan, Allergy, MoodLog
 

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'birth_date', 'weight_kg', 'photo', 'notes']
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['pet', 'vaccine_name', 'date_administered', 'next_due', 'notes']
        widgets = {
            'date_administered': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'next_due': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'vaccine_name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
        }
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medicine_name", "dosage", "prescribed_on", "notes"]
        widgets = {
            'prescribed_on': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['condition', 'description', 'date_diagnosed', 'treatment']
        widgets = {
            'date_diagnosed': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
        }

# class DietPlanForm(forms.ModelForm):
#     class Meta:
#         model = DietPlan
#         fields = ["food_item", "quantity", "time_of_day", "notes"]

from django import forms
from .models import DietPlan

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ["food_type", "food_item", "quantity", "time_of_day", "meal_date", "notes"]
        widgets = {
            "food_type": forms.Select(attrs={"class": "form-control"}),
            "food_item": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.TextInput(attrs={"class": "form-control"}),
            "time_of_day": forms.Select(attrs={"class": "form-control"}),
            "meal_date": forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ["allergen", "reaction", "severity"]

class MoodLogForm(forms.ModelForm):
    class Meta:
        model = MoodLog
        fields = ["mood", "log_date", "notes"]
        widgets = {
            "mood": forms.Select(attrs={"class": "form-control"}),
            "log_date": forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Adding context like environment or triggers..."})
        }

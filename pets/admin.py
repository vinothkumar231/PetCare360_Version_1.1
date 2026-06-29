from django.contrib import admin
from .models import Pet, Vaccination

class VaccinationInline(admin.TabularInline):
    model = Vaccination
    extra = 1

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'species', 'breed', 'age_years', 'weight_kg')
    search_fields = ('name', 'breed', 'owner__username', 'owner__email')
    list_filter = ('species',)
    inlines = [VaccinationInline]

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'vaccine_name', 'date_administered', 'next_due')
    search_fields = ('vaccine_name', 'pet__name')
    list_filter = ('date_administered',)

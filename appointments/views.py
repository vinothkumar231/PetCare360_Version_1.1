from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment
from pets.models import Pet   # ✅ import Pet from the pets app

# -------------------------
# Pet Owner Views
# -------------------------

 
#  def book_appointment(request, pet_id):
#     """Pet Owner books an appointment for their pet"""
#     pet = get_object_or_404(Pet, id=pet_id, owner=request.user)

#     if request.method == "POST":
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.pet = pet
#             appointment.owner = request.user
#             appointment.status = 'pending'
#             appointment.save()
#             messages.success(request, "Appointment booked successfully ✅")
#             return redirect("appointment_list")
#     else:
#         form = AppointmentForm()

#     return render(request, "appointments/book_appointment.html", {"form": form, "pet": pet})
# def book_appointment(request, pet_id=None):
#     pet = Pet.objects.get(id=pet_id) if pet_id else None

#     if request.method == 'POST':
#         form = AppointmentForm(request.POST, user=request.user)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.owner = request.user
#             if pet:
#                 appointment.pet = pet
#             appointment.save()
#             return redirect('appointment_list')
#     else:
#         form = AppointmentForm(user=request.user)

#     return render(request, 'appointments/book_appointment.html', {
#         'form': form,
#         'pet': pet
#     })
@login_required
def book_appointment(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.owner = request.user
            appointment.pet = pet
            appointment.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(user=request.user)

    return render(request, 'appointments/book_appointment.html', {'form': form, 'pet': pet})



@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(owner=request.user)
    return render(request, "appointments/appointment_list.html", {"appointments": appointments})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk, owner=request.user)
    appointment.delete()
    messages.success(request, "Appointment canceled successfully.")
    return redirect("appointments:appointment_list")

@login_required
def reschedule_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk, owner=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment, user=request.user)
    return render(request, 'appointments/book_appointment.html', {'form': form, 'pet': appointment.pet})

# def appointment_list(request, pet_id):
#     pet = Pet.objects.get(id=pet_id)
#     appointments = Appointment.objects.filter(pet=pet)
#     return render(
#         request,
#         "appointments/appointment_list.html",
#         {"appointments": appointments, "pet": pet}
#     )
# def appointment_list(request):
#     """Pet Owner views only their own appointments"""
#     # appointments = Appointment.objects.filter(pet_id=pet_id) 
#     # appointments = Appointment.objects.filter(owner=request.user).order_by("-date")
#     appointments = Appointment.objects.all()
#     return render(request, "appointments/appointment_list.html", {"appointments": appointments })


# -------------------------
# Vet (Service Provider) Views
# -------------------------

@login_required
def vet_dashboard(request):
    """Vet views all appointments assigned to them"""
    if not request.user.is_vet:
        messages.error(request, "You are not authorized to access the vet dashboard.")
        return redirect("appointments:appointment_list")

    appointments = Appointment.objects.filter(vet=request.user).order_by("date")
    return render(request, "appointments/vet_dashboard.html", {"appointments": appointments})


@login_required
def manage_appointment(request, appointment_id, action):
    """Vet manages appointment status (accept/reject/complete)"""
    appointment = get_object_or_404(Appointment, id=appointment_id, vet=request.user)

    if action == "accept":
        appointment.status = "accepted"
    elif action == "reject":
        appointment.status = "rejected"
    elif action == "complete":
        appointment.status = "completed"

    appointment.save()
    messages.success(request, f"Appointment {action}ed successfully ✅")
    return redirect("appointments:vet_dashboard")

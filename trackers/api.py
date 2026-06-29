import math
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PetLocation, Geofence, LocationAlert
from pets.models import Pet
from django.shortcuts import get_object_or_404
from django.utils import timezone

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_location(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')
    
    if lat is None or lon is None:
        return Response({'success': False, 'error': 'Missing coordinates'}, status=400)
    
    location = PetLocation.objects.create(pet=pet, latitude=float(lat), longitude=float(lon))
    
    # Check Geofences
    geofences = Geofence.objects.filter(pet=pet, is_active=True)
    alerts_generated = False
    for fence in geofences:
        distance = haversine(location.latitude, location.longitude, fence.center_latitude, fence.center_longitude)
        if distance > fence.radius_meters:
            # Check if there's already an active alert to prevent spamming
            recent_alert = LocationAlert.objects.filter(pet=pet, is_resolved=False).exists()
            if not recent_alert:
                LocationAlert.objects.create(
                    pet=pet,
                    message=f"{pet.name} left the '{fence.name}' geofence! (Distance: {int(distance)}m)"
                )
                alerts_generated = True
            
    return Response({'success': True, 'alerts_generated': alerts_generated})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_location_history(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    limit = int(request.GET.get('limit', 50))
    locations = PetLocation.objects.filter(pet=pet).order_by('-timestamp')[:limit]
    
    data = []
    for loc in locations:
        data.append({
            'lat': loc.latitude,
            'lng': loc.longitude,
            'timestamp': loc.timestamp.isoformat()
        })
    return Response({'success': True, 'locations': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_alerts(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    recent_alerts = LocationAlert.objects.filter(pet=pet, is_resolved=False).order_by('-timestamp')[:5]
    
    data = []
    for alert in recent_alerts:
        data.append({
            'id': alert.id,
            'message': alert.message,
            'timestamp': alert.timestamp.isoformat()
        })
    return Response({'success': True, 'alerts': data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_alerts(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    LocationAlert.objects.filter(pet=pet, is_resolved=False).update(is_resolved=True)
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_geofence(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    lat = request.data.get('latitude')
    lon = request.data.get('longitude')
    radius = request.data.get('radius', 100)
    
    if lat is None or lon is None:
        return Response({'success': False, 'error': 'Missing coordinates'}, status=400)
        
    fence, created = Geofence.objects.update_or_create(
        pet=pet,
        name='Default Geofence',
        defaults={'center_latitude': float(lat), 'center_longitude': float(lon), 'radius_meters': int(radius), 'is_active': True}
    )
    return Response({'success': True, 'message': 'Geofence updated'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_geofence(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    fence = Geofence.objects.filter(pet=pet, name='Default Geofence').first()
    if fence:
        return Response({
            'success': True, 
            'geofence': {
                'lat': fence.center_latitude,
                'lng': fence.center_longitude,
                'radius': fence.radius_meters
            }
        })
    return Response({'success': False, 'error': 'No geofence found'})

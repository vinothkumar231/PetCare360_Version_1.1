from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pets.urls')),
    path("appointments/", include("appointments.urls", namespace="appointments")),
    path('medical/', include('medical.urls')),
    path("", include('recommendations.urls')),
    path('trackers/', include('trackers.urls', namespace='trackers')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

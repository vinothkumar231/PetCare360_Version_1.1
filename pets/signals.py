import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Pet


@receiver(post_delete, sender=Pet)
def delete_pet_image(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
           os.remove(instance.photo.path)
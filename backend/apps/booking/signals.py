from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def mark_apartment_unavailable(sender, instance, **kwargs):
    apartment = instance.apartment
    apartment.availability = False
    apartment.save()

@receiver(post_delete, sender=Booking)
def mark_apartment_available(sender, instance, **kwargs):
    apartment = instance.apartment
    apartment.availability = True
    apartment.save()

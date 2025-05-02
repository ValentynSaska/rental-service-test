from django.db import models
from apps.apartments.models import Apartment
from apps.users.models import User

class Booking(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
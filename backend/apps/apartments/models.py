from django.db import models

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='apartments/')  # Зберігається в папці media/apartments
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2) 
    number_of_rooms = models.IntegerField()
    square = models.DecimalField(max_digits=8, decimal_places=2) 
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

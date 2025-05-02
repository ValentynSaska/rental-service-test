from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'user')  # Поля, які будуть відображатися в списку
    search_fields = ('apartment__name', 'user__username')  # Поля для пошуку
    list_filter = ('apartment', 'user')  # Фільтри за цими полями
    ordering = ('-id',)  # Сортування за ID (за спадаючим порядком)


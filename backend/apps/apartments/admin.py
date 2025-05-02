from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Apartment

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'number_of_rooms', 'square', 'availability', 'created_at', 'updated_at', 'image')
    list_filter = ('availability', 'created_at', 'number_of_rooms')
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)} 
    ordering = ('-created_at',)
    
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No image"

    image_tag.short_description = 'Image'

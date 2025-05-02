from rest_framework import serializers
from apps.booking.models import Booking
from apps.apartments.models import Apartment
from apps.users.models import User

class BookingSerializer(serializers.ModelSerializer):
    apartment_name = serializers.CharField(source='apartment.name', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'apartment_name', 'user_first_name', 'apartment', 'user']  # додаємо нові поля
        read_only_fields = ['user', 'apartment']

    def create(self, validated_data):
        """
        Автоматично присвоює поточного користувача при створенні бронювання.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

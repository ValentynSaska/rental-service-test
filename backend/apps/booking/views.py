from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.booking.models import Booking
from apps.booking.serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models import Apartment
from django.shortcuts import get_object_or_404

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Повертаємо:
        - Якщо користувач є адміністратором, то всі бронювання.
        - Якщо користувач не адміністратор, то тільки свої бронювання.
        """
        user = self.request.user
        if user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        apartment_id = self.request.data.get('apartment')
        apartment = get_object_or_404(Apartment, id=apartment_id)

        serializer.save(apartment=apartment, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Дозволяємо користувачеві видаляти лише свої бронювання.
        """
        booking = self.get_object()
        if booking.user != request.user:
            return Response({"detail": "You can only delete your own bookings."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

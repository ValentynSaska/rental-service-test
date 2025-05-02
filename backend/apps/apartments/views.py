from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Apartment
from .serializers import ApartmentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse




class ApartmentListView(generics.ListAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search = self.request.query_params.get('search')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        rooms_min = self.request.query_params.get('rooms_min')
        rooms_max = self.request.query_params.get('rooms_max')
        available = self.request.query_params.get('available')
        page = self.request.query_params.get('page')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if price_min:
            try:
                price_min = float(price_min)
                queryset = queryset.filter(price__gte=price_min)
            except ValueError:
                pass  

        if price_max:
            try:
                price_max = float(price_max)
                queryset = queryset.filter(price__lte=price_max)
            except ValueError:
                pass  

        if rooms_min:
            try:
                rooms_min = int(rooms_min)
                queryset = queryset.filter(number_of_rooms__gte=rooms_min)
            except ValueError:
                pass
            
        if rooms_max:
            try:
                rooms_max = int(rooms_max)
                queryset = queryset.filter(number_of_rooms__lte=rooms_max)
            except ValueError:
                pass

        if available:
            if available.lower() == 'true':
                queryset = queryset.filter(availability=True)
            elif available.lower() == 'false':
                pass
            
        return queryset


class ApartmentDetailView(RetrieveAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    lookup_field = 'slug'

class ApartmentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug):
        try:
            apartment = Apartment.objects.get(slug=slug)
        except Apartment.DoesNotExist:
            return JsonResponse({'error': 'Apartment not found'}, status=404)

        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete apartments.")

        apartment.delete()
        return JsonResponse({'message': 'Apartment deleted successfully'}, status=204)


class ApartmentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, slug):
        try:
            apartment = Apartment.objects.get(slug=slug)
        except Apartment.DoesNotExist:
            raise NotFound("Apartment not found.")

        if not request.user.is_staff:
            raise PermissionDenied("Only admin users can update apartments.")

        data = request.data.copy()
        if 'image' in data:
            data.pop('image')

        serializer = ApartmentSerializer(apartment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
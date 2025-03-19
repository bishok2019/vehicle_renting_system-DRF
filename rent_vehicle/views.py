from django.shortcuts import render
from .models import Customer
from vehicle.models import Vehicle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RentVehicleSerializer
# Create your views here.

class RentVehicleView(APIView): #register view to rent vehicle
    serializer_class = RentVehicleSerializer
    permission_classes = [AllowAny]
    def post(self, request, pk=None):
        serializer=RentVehicleSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({'status':'success','message':'Your request to rent vehicle has been submitted.', 'data':RentVehicleSerializer(customer).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
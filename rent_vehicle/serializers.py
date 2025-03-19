from rest_framework import serializers
from .models import Vehicle, Customer

class RentVehicleSerializer(serializers.ModelSerializer):
    # vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), many=True)
    class Meta:
        model=Customer
        fields=['customer_name', 'customer_phone_num', 'customer_email', 'customer_photo','renting_vehicle', 'rental_start_date', 'rental_end_date']
        read_only_fields=[]
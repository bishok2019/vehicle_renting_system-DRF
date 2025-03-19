from rest_framework import serializers
from .models import Category, FuelType, TransmissionType, Location, Vehicle, SluggedModel

# Base Serializers
class TimeStampedModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['created_at', 'updated_at']

class SluggedModelSerializer(TimeStampedModelSerializer):
    class Meta(TimeStampedModelSerializer.Meta):
        model = SluggedModel
        fields = TimeStampedModelSerializer.Meta.fields + ['name', 'slug']

# Model-Specific Serializers
class CategorySerializer(SluggedModelSerializer):
    class Meta(SluggedModelSerializer.Meta):
        model = Category
        fields = SluggedModelSerializer.Meta.fields + ['description']

class FuelTypeSerializer(SluggedModelSerializer):
    class Meta(SluggedModelSerializer.Meta):
        model = FuelType
        fields = SluggedModelSerializer.Meta.fields

class TransmissionTypeSerializer(SluggedModelSerializer):
    class Meta(SluggedModelSerializer.Meta):
        model = TransmissionType
        fields = SluggedModelSerializer.Meta.fields

class LocationSerializer(SluggedModelSerializer):
    class Meta(SluggedModelSerializer.Meta):
        model = Location
        fields = SluggedModelSerializer.Meta.fields + ['address', 'city', 'state', 'zip_code']

class VehicleSerializer(TimeStampedModelSerializer):

    class Meta(TimeStampedModelSerializer.Meta):
        model = Vehicle
        fields = [
            'id','make', 'model', 'year', 'registration_number', 'slug',
            'category', 'fuel_type', 'transmission', 'seating_capacity',
            'color', 'mileage', 'location', 'is_available', 'daily_rate',
            'fuel_efficiency', 'features'
        ] + TimeStampedModelSerializer.Meta.fields
        read_only_fields = ['slug']
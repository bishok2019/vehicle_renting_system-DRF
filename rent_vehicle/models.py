#visitor_app/models.py
from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from vehicle.models import User, VehicleAvailability, Vehicle, Location

# Create your models here.
class Customer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked-In'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=150)
    customer_phone_num = models.CharField(max_length=15,null=True, blank=True, unique=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_photo = models.ImageField(upload_to='customer_photos/',null=True, blank=True)
    renting_vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name='vehicle')
    rental_start_date = models.DateField()
    rental_end_date = models.DateField()
    rental_start_time = models.TimeField()
    rental_end_time = models.TimeField()
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    customer_location =models.ForeignKey(Location, on_delete=models.CASCADE)
    vehicle_delievery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # vehicle_availability = models.ForeignKey(VehicleAvailability, on_delete=models.SET_NULL, null=True, blank=True, related_name='availabilities')

    def __str__(self):
        return self.name

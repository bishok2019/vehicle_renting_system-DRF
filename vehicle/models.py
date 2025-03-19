from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User
# --- Abstract Base Models ---
class TimeStampedModel(models.Model):
    """Base model providing automatic timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Prevents database table creation for this base model


class SluggedModel(TimeStampedModel):
    """Base model adding name/slug functionality with automatic slug creation"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        """Automatically generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Human-readable representation

    class Meta(TimeStampedModel.Meta): # Inheriting abstract=True
        ordering = ['name']  # Overriding Parent's ordering, implementing default


# --- Vehicle Specifications ---
class Category(SluggedModel):
    """Vehicle classification (e.g., SUV, Sedan)"""
    description = models.TextField(blank=True)
    
    class Meta(SluggedModel.Meta):
        verbose_name_plural = "Categories"  # Fixes admin panel display name


class FuelType(SluggedModel):
    """Power source types (e.g., Gasoline, Electric)"""
    # Inherits all SluggedModel functionality
    pass


class TransmissionType(SluggedModel):
    """Gear system types (e.g., Automatic, Manual)"""
    # Inherits all SluggedModel functionality
    pass


# --- Location Management ---
class Location(SluggedModel):
    """Physical storage locations for vehicles"""
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    class Meta(SluggedModel.Meta):
        verbose_name_plural = "Locations"  # Fixes admin panel display name


# --- Main Vehicle Model ---
class Vehicle(TimeStampedModel):
    """Concrete model representing a rentable vehicle"""
    # Core Identification
    make = models.CharField(max_length=100)  # Manufacturer
    model = models.CharField(max_length=100)  # Model name
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),  # No vehicles before 1900
            MaxValueValidator(2100)   # Future-proof year validation
        ]
    )
    registration_number = models.CharField(
        max_length=20, 
        unique=True  # Prevent duplicate registrations
    )
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    # Technical Specifications
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,  # Allow null if category is deleted
        related_name='vehicle_category'
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicles_fuel_type'
    )
    transmission = models.ForeignKey(
        TransmissionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicles_transmission'
    )
    seating_capacity = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()  # Current odometer reading

    # Rental Business Logic
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicles_location'
    )
    is_available = models.BooleanField(
        default=True,
        db_index=True  # Faster filtering for availability
    )
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]  # Prevent negative prices
    )

    # Optional Technical Details
    fuel_efficiency = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Fuel efficiency in km/l or mpg"
    )
    features = models.TextField(
        blank=True,
        help_text="Comma-separated list of special features"
    )

    def save(self, *args, **kwargs):
        """Auto-generate slug from vehicle details"""
        if not self.slug:
            base_slug = f"{self.year}-{self.make}-{self.model}-{self.registration_number}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        """Human-readable vehicle identification"""
        return f"{self.year} {self.make} {self.model} ({self.registration_number})"

    class Meta:
        """Vehicle-specific configurations"""
        ordering = ['-created_at']  # Show newest vehicles first by default
        indexes = [
            # Optimize common search combinations
            models.Index(fields=['make', 'model']),
            # Speed up availability filtering
            models.Index(fields=['is_available']),
            # Quick registration number lookups
            models.Index(fields=['registration_number']),
        ]
        verbose_name_plural = "Vehicles"  # Admin panel plural name


class VehicleAvailability(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_approved = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    
    @classmethod
    def find_available_coverage(cls, vehicle, date, start_time, end_time,exclude_slot=None):
        slots = cls.objects.filter(
            vehicle=vehicle,
            date=date,
            # is_booked=False,
            is_approved=True,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).order_by('start_time').exclude(id=exclude_slot.id if exclude_slot else None)

        coverage = []
        current_start = start_time
        for slot in slots:
            # Include slots that contain the current_start, even if they start before it
            if slot.end_time > current_start:
                coverage_end = min(slot.end_time, end_time)
                coverage.append({
                    'slot': slot,
                    'start': max(slot.start_time, current_start),
                    'end': coverage_end
                })
                current_start = coverage_end
                if current_start >= end_time:
                    return coverage
        return None if not coverage else coverage
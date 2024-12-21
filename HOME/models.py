from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime, time

class Dessert(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='desserts/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Beverage(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='beverages/', null=True, blank=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='food/', null=True, blank=True)

    def __str__(self):
        return self.name

class Breakfast(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='breakfast/', null=True, blank=True)

    def __str__(self):
        return self.name

class Snacks(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='snacks/', null=True, blank=True)

    def __str__(self):
        return self.name

class Bakeryitem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='bakery-items/', null=True, blank=True)

    def __str__(self):
        return self.name

class Billing(models.Model):
    # Link to the user who made the purchase
    customer = models.ForeignKey(
        get_user_model(),  # Refers to the currently configured user model
        on_delete=models.CASCADE,  # Deletes billings if the user is deleted
        related_name='billings'
    )
    # Store purchased items (name, quantity, price) as JSON
    items = models.JSONField()  
    # Total cost of the purchase
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    # Date and time of billing
    timestamp = models.DateTimeField(auto_now_add=True)  
    receipt_content = models.TextField(null=True, blank=True)  # Stores receipt HTML:

    def __str__(self):
        receipt_status = "with Receipt" if self.receipt_content else "without Receipt"
        return f"Billing #{self.id} - {self.customer.username} - ₹{self.total_price} ({receipt_status})"

class Table(models.Model):
    number = models.PositiveIntegerField() 
    seats = models.PositiveIntegerField()  # Number of seats at the table
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)  # Cost per hour
    is_available = models.BooleanField(default=True)  # Admin can manually mark availability
    available_from = models.TimeField(default=time(8, 0))  # Default available from 8 AM
    available_to = models.TimeField(default=time(22, 0))  # Default available to 10 PM

    def __str__(self):
        return f"Table {self.number} - Seats: {self.seats} - ₹{self.price_per_hour}/hour"

    def is_time_slot_available(self, booking_time, duration):
        """
        Check if the table is available at the requested time and duration.
        """
        booking_end_time = (datetime.combine(datetime.today(), booking_time) + duration).time()
        return self.available_from <= booking_time <= self.available_to and self.available_from <= booking_end_time <= self.available_to

class TableBookings(models.Model):
    # Link to the user who made the booking
    customer = models.ForeignKey(
        get_user_model(),  # Refers to the currently configured user model
        on_delete=models.CASCADE,  # Deletes bookings if the user is deleted
        related_name='table_bookings'
    )
    # Store booked tables as a Many-to-Many relationship (Not JSON)
    tables = models.ManyToManyField(Table, related_name='bookings')  
    # Total cost of the booking
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    # Date and time of booking creation
    timestamp = models.DateTimeField(auto_now_add=True)  
    # Date and time of the actual booking
    booking_date = models.DateField()  
    booking_time = models.TimeField()  
    # Duration of the booking
    duration = models.DurationField()  
    # Contact information
    contact_number = models.CharField(max_length=15)  

    def __str__(self):
        return f"TableBooking #{self.id} by {self.customer.username} for ₹{self.total_price}"

from django.contrib import admin
from .models import Dessert, Bakeryitem, Billing, Table, Beverage, Food, Breakfast, Snacks, TableBookings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.html import format_html
from django.urls import reverse

# Register Dessert Model
admin.site.register(Dessert)
admin.site.register(Beverage)
admin.site.register(Food)
admin.site.register(Breakfast)
admin.site.register(Snacks)
# Register Bakeryitem Model with custom admin
@admin.register(Bakeryitem)
class BakeryitemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)

# Custom User Admin to display login status
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'is_active', 'is_logged_in')

    # Method to display user's login status
    def is_logged_in(self, obj):
        if obj.last_login and (now() - obj.last_login).total_seconds() < 300:
            return 'Yes'  # User is logged in (last login within 5 minutes)
        return 'No'  # User is not logged in
    is_logged_in.short_description = 'Logged In'

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register Billing Model with custom admin
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'timestamp', 'view_receipt_link')  # Added link to view receipt
    list_filter = ('timestamp',)  # Filter by timestamp
    search_fields = ('customer__username', 'id')  # Search by customer and billing ID
    readonly_fields = ('timestamp', 'view_items', 'receipt_content_display')  # Make receipt and timestamp readonly

    # Format the display of items in the admin panel
    def view_items(self, obj):
        """
        A readable format for the items field, showing each item's name, quantity, and price.
        """
        items = obj.items
        if not items:
            return 'No items found'
        return '\n'.join([f"{item['name']} - Qty: {item['quantity']} - ₹{item['totalPrice']}" for item in items])
    view_items.short_description = 'Purchased Items'

    # Display receipt content in a readable format
    def receipt_content_display(self, obj):
        """
        Shows the receipt's content in a readable format.
        """
        if obj.receipt_content:
            return format_html(obj.receipt_content)
        return "No receipt available"
    receipt_content_display.short_description = 'Receipt Content'

    # Provide a link to view the receipt in a new tab
    def view_receipt_link(self, obj):
        if obj.receipt_content:
            url = reverse('view_receipt', args=[obj.id])  # Match the name of your URL pattern
            return format_html('<a href="{}" target="_blank">View Receipt</a>', url)
        return "No Receipt"
    view_receipt_link.short_description = 'Receipt'

    # Define the fields shown on the detail view page
    fields = ('customer', 'total_price', 'timestamp', 'view_items', 'receipt_content_display')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats', 'price_per_hour', 'is_available', 'available_from', 'available_to')
    list_filter = ('is_available',)
    search_fields = ('number', 'seats')

    fieldsets = (
        (None, {
            'fields': ('number', 'seats', 'price_per_hour', 'is_available', 'available_from', 'available_to')
        }),
    )

@admin.register(TableBookings)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'booking_date', 'booking_time', 'duration', 'total_price')
    list_filter = ('booking_date',)
    search_fields = ('customer__username', 'contact_number')
    filter_horizontal = ('tables',)  # Allows selecting tables via a multi-select interface
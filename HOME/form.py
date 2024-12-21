from django import forms
from .models import Table, TableBookings
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError

class BookingForm(forms.Form):
    booking_date = forms.DateField(widget=forms.SelectDateWidget)
    booking_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    contact_number = forms.CharField(max_length=15)

    # Dropdown for hours
    hours = forms.ChoiceField(choices=[(i, f"{i} hour{'s' if i > 1 else ''}") for i in range(0, 12)], label="Hours")
    # Dropdown for minutes
    minutes = forms.ChoiceField(choices=[(i, f"{i} minute{'s' if i > 1 else ''}") for i in range(0, 60, 15)], label="Minutes")

    # Tables selection - multiple choice
    tables = forms.ModelMultipleChoiceField(queryset=Table.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    def clean(self):
        cleaned_data = super().clean()
        hours = int(cleaned_data.get('hours', 0))
        minutes = int(cleaned_data.get('minutes', 0))

        # Combine hours and minutes into a timedelta
        duration = timedelta(hours=hours, minutes=minutes)

        # Validate the minimum duration
        if duration < timedelta(hours=1):
            raise forms.ValidationError("Booking duration must be at least 1 hour.")

        # Ensure the booking date is in the future
        booking_date = cleaned_data.get('booking_date')
        if booking_date and booking_date < datetime.today().date():
            raise forms.ValidationError("Booking date must be in the future.")
        
        # Ensure at least one table is selected
        selected_tables = cleaned_data.get('tables')
        if not selected_tables:
            raise forms.ValidationError("You must select at least one table.")
        
        # Validate that the selected tables are available for the chosen date and time
        booking_time = cleaned_data.get('booking_time')
        if booking_date and booking_time:
            conflicting_bookings = TableBookings.objects.filter(
                booking_date=booking_date,
                booking_time=booking_time,
                tables__in=selected_tables
            )
            if conflicting_bookings.exists():
                raise forms.ValidationError("One or more selected tables are already booked for this time.")

        # Add the combined duration to cleaned data
        cleaned_data['duration'] = duration
        return cleaned_data

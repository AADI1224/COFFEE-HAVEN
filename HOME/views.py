from django.shortcuts import render, HttpResponse, redirect
from urllib.parse import quote
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import Dessert, Bakeryitem, Billing, TableBookings, Beverage, Food, Breakfast, Snacks, Table
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from .form import BookingForm
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import F
from decimal import Decimal

# Home Page
def home(request):
    return HttpResponse("<h1>Hello! I'm AADITYA CHOUHAN</h1>")

# About Us Page
def about_us(request):
    return render(request, "aboutus.html")

# Template Example
def template1(request):
    recipient_email = "chouhannikhil924254@gmail.com"
    subject = "Inquiry about the service"
    phone_number = "6269341024"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(recipient_email)}&su={quote(subject)}"
    return render(request, "1.html", context={'gmail_url': gmail_url, 'phone_number': phone_number})

def about_us(request):
    recipient_email = "chouhannikhil924254@gmail.com"
    subject = "Inquiry about the service"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(recipient_email)}&su={quote(subject)}"
    return render(request, "aboutus.html", context={'gmail_url': gmail_url})

# Menu Pages
def BakeryItem(request):
    bakeryitem = Bakeryitem.objects.all()
    return render(request, 'bakery-items.html', {'bakeryitem': bakeryitem})

def Desserts(request):
    desserts = Dessert.objects.all()
    return render(request, 'desserts.html', {'desserts': desserts})

def Beverages(request):
    beverages = Beverage.objects.all()
    return render(request, 'beverages.html', {'beverages': beverages})

def Foods(request):
    food = Food.objects.all()
    return render(request, 'food.html', {'food': food})

def Breakfasts(request):
    breakfast = Breakfast.objects.all()
    return render(request, 'breakfast.html', {'breakfast': breakfast})

def Snack(request):
    snacks = Snacks.objects.all()
    return render(request, 'snacks.html', {'snacks': snacks})

# Cart Page
def cart(request):
    if not request.user.is_authenticated:
        # Redirect to the cart page with a login prompt
        return render(request, 'cart.html', {'login_required': True})
    
    # User is authenticated, proceed as normal
    cart = request.session.get('cart', [])
    total_price = sum(item['totalPrice'] for item in cart)
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price, 'login_required': False})


@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))  # Ensure price is treated as a float
        img = request.POST.get('img')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is specified

        # Get the cart from the session
        cart = request.session.get('cart', [])

        # Check if the item already exists in the cart
        existing_item = next((item for item in cart if item['name'] == name), None)

        if existing_item:
            # Item exists, update the quantity and total price
            existing_item['quantity'] += quantity
            existing_item['totalPrice'] = existing_item['quantity'] * existing_item['price']
        else:
            # Item does not exist, add new item to the cart with total price
            total_price = price * quantity
            cart.append({
                'name': name,
                'price': price,
                'img': img,
                'quantity': quantity,
                'totalPrice': total_price  # Add totalPrice to the item
            })

        # Save the updated cart to the session
        request.session['cart'] = cart

        # Mark session as modified to ensure updates are saved
        request.session.modified = True

        # Return the updated cart and cart count
        return JsonResponse({
            'cart': cart,
            'cartCount': len(cart)
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        cart = request.session.get('cart', [])

        # Filter out the item to be removed
        cart = [item for item in cart if item['name'] != item_name]
        
        # Update the session with the modified cart
        request.session['cart'] = cart

        # Mark session as modified to ensure updates are saved
        request.session.modified = True

        # Return the updated cart
        if not cart:
            return JsonResponse({'cart': [], 'message': 'Your cart is now empty.'})

        return JsonResponse({'cart': cart, 'message': f'{item_name} removed from the cart.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Login View
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and login the user
            user = form.get_user()
            auth_login(request, user)
            # Redirect to the home page or to a 'next' URL
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error': None})

# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']  # Confirm password

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'signup.html')

def Logout(request):
    logout(request)  # Logs out the user
    return redirect('/')  # Redirect the user to the home page

def get_cart_count(request):
    # Get the cart from the session
    cart = request.session.get('cart', [])

    # Return the count of items in the cart
    return JsonResponse({'cartCount': len(cart)})

@csrf_exempt
@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])

        # Check if the cart is empty
        if not cart:
            return JsonResponse({'error': 'No items in the cart'}, status=400)

        # Calculate the total price
        total_price = sum(item['quantity'] * item['price'] for item in cart)

        # Create the billing record
        billing = Billing.objects.create(
            customer=request.user,
            total_price=total_price
        )

        # Save each cart item in the billing
        for item in cart:
            Billing.objects.create(
                billing=billing,
                name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                total_price=item['quantity'] * item['price']
            )

        # Clear the cart session
        request.session['cart'] = []

        # Return the receipt URL
        receipt_url = reverse('receipt', args=[billing.id])
        return JsonResponse({'url': receipt_url})

    # If GET request or invalid request
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@login_required
def receipt(request, billing_id):
    try:
        billing = Billing.objects.get(id=billing_id, customer=request.user)
        return render(request, 'receipt.html', {'billing': billing})
    except Billing.DoesNotExist:
        return HttpResponseBadRequest("Receipt not found.")

def view_receipt(request, billing_id):
    """
    View receipt in the admin panel.
    """
    
    billing = get_object_or_404(Billing, id=billing_id)

    # Check if the user is an admin
    is_admin = request.user.is_staff

    return render(request, 'receipt.html', {'billing': billing, 'is_admin': is_admin})

@login_required
def book_table(request):
    # Get the available tables (those that are marked as is_available=True)
    available_tables = Table.objects.filter(is_available=True)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            # Get the form data
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            contact_number = form.cleaned_data['contact_number']
            selected_tables = form.cleaned_data['tables']
            duration = form.cleaned_data['duration']
            
            # Calculate total price based on selected tables and duration
            total_price = Decimal(0)  # Initialize total price as Decimal

            # Add price for each selected table
            for table in selected_tables:
                total_price += table.price_per_hour

            # Convert duration (in seconds) to hours and multiply by total price
            total_price *= Decimal(duration.total_seconds()) / Decimal(3600)

            # Create a new booking in the TableBookings model
            booking = TableBookings.objects.create(
                customer=request.user,
                booking_date=booking_date,
                booking_time=booking_time,
                contact_number=contact_number,
                duration=duration,
                total_price=total_price
            )

            # Add the selected tables to the booking
            booking.tables.set(selected_tables)

            # Provide success message
            messages.success(request, "Your booking was successful!")

            return redirect('success_page')  # Redirect to a success page after saving the booking
        else:
            messages.error(request, "There was an error with your booking.")
    else:
        form = BookingForm()

    # Pass available tables along with the form to the template
    return render(request, 'book_table.html', {
        'form': form,
        'available_tables': available_tables
    })

def get_available_tables(booking_date, booking_time, duration):
    # Combine the booking date and time to get the start datetime
    booking_start = datetime.combine(booking_date, booking_time)

    # Calculate the booking end time
    booking_end = booking_start + duration

    # Get IDs of tables with overlapping bookings
    booked_table_ids = TableBookings.objects.filter(
        booking_date=booking_date
    ).filter(
        # Ensure no overlap in time
        booking_time__lt=booking_end.time(),  # Booking starts before requested end time
        booking_time__gt=booking_start.time()  # Booking ends after requested start time
    ).values_list('tables', flat=True)

    # Fetch tables that are not booked, are marked as available, and are within the available time range
    available_tables = Table.objects.exclude(id__in=booked_table_ids).filter(
        is_available=True
    ).filter(
        # Ensure table's available time slot fits the requested booking time
        available_from__lte=booking_time, 
        available_to__gte=(booking_start + duration).time()
    )

    return available_tables
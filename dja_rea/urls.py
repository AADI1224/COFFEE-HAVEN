from django.contrib import admin
from django.urls import path
from HOME.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aboutus/', about_us, name="aboutus"),
    path('', template1, name="template1"),
    path('bakery-items/', BakeryItem, name="BakeryItems"),
    path('desserts/', Desserts, name="Desserts"),
    path('beverages/', Beverages, name="Beverages"),
    path('food/', Foods, name="Food"),
    path('breakfast/', Breakfasts, name="Breakfast"),
    path('snacks/', Snack, name="Snacks"),   
    path('cart/', cart, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', Logout, name='logout'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('checkout/', checkout, name='checkout'),
    path('receipt/<int:billing_id>/', receipt, name='receipt'),
    path('view_receipt/<int:billing_id>/', view_receipt, name='view_receipt'),
    path('book-table/', book_table, name='book_table'),
]

# Add media URL configuration for serving uploaded files during development
if settings.DEBUG:  # Ensure this is only active in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

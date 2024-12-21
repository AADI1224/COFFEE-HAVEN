from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.http import HttpResponse

class SeparateSessionMiddleware(MiddlewareMixin):
    """
    Middleware to separate session storage for Django admin users
    and regular users by dynamically modifying the session engine
    and cookie name based on the port.
    """
    def process_request(self, request):
        # Get the port number from the request
        port = request.META.get('SERVER_PORT', '8000')

        # Default session cookie name
        session_cookie_name = 'sessionid'

        # Check if the request is for the admin panel
        current_url = resolve(request.path_info)
        
        if current_url.app_name == 'admin':  # Admin users
            session_cookie_name = f'admin_{port}_sessionid'  # Append port to cookie name
        elif request.user.is_authenticated:  # Regular authenticated users
            session_cookie_name = f'regular_{request.user.username}_{port}_sessionid'  # Append port to cookie name

        # Set the session cookie name in request
        request.META['SESSION_COOKIE_NAME'] = session_cookie_name

        # If there is no session, create a new one for the user
        if not request.COOKIES.get(session_cookie_name):
            request.session.create()

        # Store the session cookie name in the response
        response = self.get_response(request)
        response.set_cookie(session_cookie_name, request.session.session_key)
        return response

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track user activity for logged-in users
        if request.user.is_authenticated:
            # Update last login time (you can adjust this if you want to use a different field)
            User.objects.filter(id=request.user.id).update(last_login=now())
        response = self.get_response(request)
        return response
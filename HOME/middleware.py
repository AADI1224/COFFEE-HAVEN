from django.contrib.sessions.models import Session
from django.utils.timezone import now

class ClearOldSessionsMiddleware:
    """
    Middleware to clear expired sessions on each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clear expired sessions
        Session.objects.filter(expire_date__lt=now()).delete()
        return self.get_response(request)

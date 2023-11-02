from django.contrib.auth.models import User
from .models import UserDepartment

class DepartmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_department = UserDepartment.objects.filter(user=user).values('department').first()
            request.department = user_department['department'] if user_department else None
        else:
            request.department = None

        response = self.get_response(request)

        return response

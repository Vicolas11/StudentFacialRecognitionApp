
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
      
class LecturerLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an Lecture"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_lecturer:
            return redirect('facial:login_lecturer')
        return super().dispatch(request, *args, **kwargs)

class StudentLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an Student"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            return redirect('facial:login_student')
        return super().dispatch(request, *args, **kwargs)

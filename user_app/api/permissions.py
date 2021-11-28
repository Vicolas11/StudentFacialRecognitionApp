from facial_app.models import User
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == "GET" or admin_permission
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return admin_permission

class IsReveiwUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):

      def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return request.user == User.objects.get(pk=view.kwargs['pk']) or request.user.is_staff
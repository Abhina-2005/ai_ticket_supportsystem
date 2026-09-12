from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return obj.assigned_to ==request.user
        return obj.created_by==request.user

class IsCommentOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return obj.ticket.assigned_to ==request.user
        return obj.ticket.created_by==request.user

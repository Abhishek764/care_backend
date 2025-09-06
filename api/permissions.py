from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """Allow owners to modify; others read-only."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Patient objects have `created_by`; others we let view handle
        return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)
from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    """
    Faqat organizer foydalanuvchilar create/update/destroy amallarini bajara oladi.
    Oddiy userlar faqat o'qishi mumkin.
    """
    message = "Only organizers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "organizer")


class IsAdminOrReadOnly(BasePermission):
    """
    Faqat adminlar categoryni boshqarishi mumkin.
    Oddiy userlar faqat o'qishi mumkin.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_staff  # yoki `request.user.is_superuser`

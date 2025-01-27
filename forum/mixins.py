from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class ModeratorRequiredMixin(UserPassesTestMixin):
    """
    A mixin that ensures the user is a member of the "Moderatori" group.

    Methods:
        test_func(): Checks if the user is in the "Moderatori" group.
        handle_no_permission(): Raises a PermissionDenied exception if the user
                                does not have the required permissions.
    """

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return self.request.user.groups.filter(name="Moderators").exists()

    def handle_no_permission(self):
        raise PermissionDenied("You don't have permission to access this page.")

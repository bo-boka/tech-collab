from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class AuthRequiredMixin(object):
    """
    Require user authentication. If not, return to login page.
    """

    login_url = '/accounts/login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), self.login_url)

        return super(AuthRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class UserAuthMixin(AuthRequiredMixin):
    """
    Checks that user is the creator of the project. If not, return 403 error.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id is not self.get_object().founder.id:
            raise PermissionDenied

        return super(UserAuthMixin, self).dispatch(
            request, *args, **kwargs)

from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class AuthenticationFailedRu(AuthenticationFailed):
    default_detail = _('Некорректный логин или пароль')

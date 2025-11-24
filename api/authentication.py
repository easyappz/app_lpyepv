import secrets
from django.utils import timezone
from rest_framework import authentication, exceptions
from api.models import Member


class Token(object):
    """Simple token storage in Member model"""
    def __init__(self, member, key):
        self.member = member
        self.key = key


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            member = Member.objects.get(auth_token=key)
        except Member.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return (member, key)

    def authenticate_header(self, request):
        return self.keyword


def generate_token():
    """Generate a random token"""
    return secrets.token_hex(32)

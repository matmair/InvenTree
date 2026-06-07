"""Custom token authentication class for InvenTree API."""

import datetime
import hmac

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

import users.models


class ApiTokenAuthentication(TokenAuthentication):
    """Custom implementation of TokenAuthentication class, with custom features.

    Changes:
    - Tokens can be revoked
    - Tokens can expire
    """

    model = users.models.ApiToken

    def authenticate_credentials(self, key):
        """Adds additional checks to the default token authentication method."""
        # Try finding as v1 token first
        token = self.model.objects.filter(key=key, version=1).first()

        if not token:
            # Try finding as v2 token
            # Prefix is first 12 characters
            prefix = key[:12]
            tokens = self.model.objects.filter(key=prefix, version=2)

            for t in tokens:
                pepper_id = t.pepper_id
                peppers = getattr(settings, 'API_TOKEN_PEPPERS', {})
                pepper = peppers.get(pepper_id) if pepper_id else settings.SECRET_KEY

                if pepper and hmac.compare_digest(t.token_hash, t.generate_hash(key, pepper)):
                    token = t
                    break

        if not token:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        user = token.user

        if token.revoked:
            raise exceptions.AuthenticationFailed(_('Token has been revoked'))

        if token.expired:
            raise exceptions.AuthenticationFailed(_('Token has expired'))

        if token.last_seen != datetime.date.today():
            # Update the last-seen date
            token.last_seen = datetime.date.today()
            token.save()

        return (user, token)


class ExtendedOAuth2Authentication(OAuth2Authentication):
    """Custom implementation of OAuth2Authentication class to support custom scope rendering."""

"""API endpoints for social authentication with allauth."""

import logging
from importlib import import_module

from django.conf import settings
from django.urls import NoReverseMatch, include, path, reverse

from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

import InvenTree.sso
from common.models import InvenTreeSetting
from common.settings import get_global_setting
from InvenTree.helpers import str2bool
from InvenTree.mixins import CreateAPI, ListAPI, ListCreateAPI
from InvenTree.serializers import EmptySerializer, InvenTreeModelSerializer

logger = logging.getLogger('inventree')


class GenericOAuth2ApiLoginView(OAuth2LoginView):
    """Api view to login a user with a social account."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the regular login view directly."""
        return self.login(request, *args, **kwargs)


class GenericOAuth2ApiConnectView(GenericOAuth2ApiLoginView):
    """Api view to connect a social account to the current user."""

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the connect request directly."""
        # Override the request method be in connection mode
        request.GET = request.GET.copy()
        request.GET['process'] = 'connect'

        # Resume the dispatch
        return super().dispatch(request, *args, **kwargs)


def handle_oauth2(adapter: OAuth2Adapter):
    """Define urls for oauth2 endpoints."""
    return [
        path(
            'login/',
            GenericOAuth2ApiLoginView.adapter_view(adapter),
            name=f'{provider.id}_api_login',
        ),
        path(
            'connect/',
            GenericOAuth2ApiConnectView.adapter_view(adapter),
            name=f'{provider.id}_api_connect',
        ),
    ]


legacy = {
    'twitter': 'twitter_oauth2',
    'bitbucket': 'bitbucket_oauth2',
    'linkedin': 'linkedin_oauth2',
    'vimeo': 'vimeo_oauth2',
    'openid': 'openid_connect',
}  # legacy connectors


# Collect urls for all loaded providers
social_auth_urlpatterns = []

provider_urlpatterns = []

for name, provider in providers.registry.provider_map.items():
    try:
        prov_mod = import_module(provider.get_package() + '.views')
    except ImportError:
        logger.exception('Could not import authentication provider %s', name)
        continue

    # Try to extract the adapter class
    adapters = [
        cls
        for cls in prov_mod.__dict__.values()
        if isinstance(cls, type)
        and cls != OAuth2Adapter
        and issubclass(cls, OAuth2Adapter)
    ]

    # Get urls
    urls = []
    if len(adapters) == 1:
        urls = handle_oauth2(adapter=adapters[0])
    elif provider.id in legacy:
        logger.warning(
            '`%s` is not supported on platform UI. Use `%s` instead.',
            provider.id,
            legacy[provider.id],
        )
        continue
    else:
        logger.error(
            'Found handler that is not yet ready for platform UI: `%s`. Open an feature request on GitHub if you need it implemented.',
            provider.id,
        )
        continue
    provider_urlpatterns += [path(f'{provider.id}/', include(urls))]


social_auth_urlpatterns += provider_urlpatterns


class SocialProviderListResponseSerializer(serializers.Serializer):
    """Serializer for the SocialProviderListView."""

    class SocialProvider(serializers.Serializer):
        """Serializer for the SocialProviderListResponseSerializer."""

        id = serializers.CharField()
        name = serializers.CharField()
        configured = serializers.BooleanField()
        login = serializers.URLField()
        connect = serializers.URLField()
        display_name = serializers.CharField()

    sso_enabled = serializers.BooleanField()
    sso_registration = serializers.BooleanField()
    mfa_required = serializers.BooleanField()
    providers = SocialProvider(many=True)
    registration_enabled = serializers.BooleanField()
    password_forgotten_enabled = serializers.BooleanField()


def registration_enabled() -> bool:
    """Return True if SSO registration is enabled."""
    return str2bool(InvenTreeSetting.get_setting('LOGIN_ENABLE_SSO_REG'))


def get_provider_app(provider):
    """Return the SocialApp object for the given provider."""
    from allauth.socialaccount.models import SocialApp

    try:
        apps = SocialApp.objects.filter(provider__iexact=provider.id)
    except SocialApp.DoesNotExist:
        logger.warning("SSO SocialApp not found for provider '%s'", provider.id)
        return None

    if apps.count() > 1:
        logger.warning("Multiple SocialApps found for provider '%s'", provider.id)

    if apps.count() == 0:
        logger.warning("SSO SocialApp not found for provider '%s'", provider.id)

    return apps.first()


def check_provider(provider):
    """Check if the given provider is correctly configured.

    To be correctly configured, the following must be true:

    - Provider must either have a registered SocialApp
    - Must have at least one site enabled
    """
    import allauth.app_settings

    # First, check that the provider is enabled
    app = get_provider_app(provider)

    if not app:
        return False

    if allauth.app_settings.SITES_ENABLED:
        # At least one matching site must be specified
        if not app.sites.exists():
            logger.error('SocialApp %s has no sites configured', app)
            return False

    # At this point, we assume that the provider is correctly configured
    return True


def provider_display_name(provider):
    """Return the 'display name' for the given provider."""
    if app := get_provider_app(provider):
        return app.name

    # Fallback value if app not found
    return provider.name


class SocialProviderListView(ListAPI):
    """List of available social providers."""

    permission_classes = (AllowAny,)
    serializer_class = EmptySerializer

    @extend_schema(
        responses={200: OpenApiResponse(response=SocialProviderListResponseSerializer)}
    )
    def get(self, request, *args, **kwargs):
        """Get the list of providers."""
        provider_list = []
        for provider in providers.registry.provider_map.values():
            provider_data = {
                'id': provider.id,
                'name': provider.name,
                'configured': False,
            }

            try:
                provider_data['login'] = request.build_absolute_uri(
                    reverse(f'{provider.id}_api_login')
                )
            except NoReverseMatch:
                provider_data['login'] = None

            try:
                provider_data['connect'] = request.build_absolute_uri(
                    reverse(f'{provider.id}_api_connect')
                )
            except NoReverseMatch:
                provider_data['connect'] = None

            provider_data['configured'] = InvenTree.sso.check_provider(provider)
            provider_data['display_name'] = InvenTree.sso.provider_display_name(
                provider
            )

            provider_list.append(provider_data)

        data = {
            'sso_enabled': str2bool(InvenTreeSetting.get_setting('LOGIN_ENABLE_SSO')),
            'sso_registration': InvenTree.sso.registration_enabled(),
            'mfa_required': settings.MFA_ENABLED
            and get_global_setting('LOGIN_ENFORCE_MFA'),
            'mfa_enabled': settings.MFA_ENABLED,
            'providers': provider_list,
            'registration_enabled': get_global_setting('LOGIN_ENABLE_REG'),
            'password_forgotten_enabled': get_global_setting('LOGIN_ENABLE_PWD_FORGOT'),
        }
        return Response(data)


class EmailAddressSerializer(InvenTreeModelSerializer):
    """Serializer for the EmailAddress model."""

    class Meta:
        """Meta options for EmailAddressSerializer."""

        model = EmailAddress
        fields = '__all__'


class EmptyEmailAddressSerializer(InvenTreeModelSerializer):
    """Empty Serializer for the EmailAddress model."""

    class Meta:
        """Meta options for EmailAddressSerializer."""

        model = EmailAddress
        fields = []


class EmailListView(ListCreateAPI):
    """List of registered email addresses for current users."""

    permission_classes = (IsAuthenticated,)
    serializer_class = EmailAddressSerializer

    def get_queryset(self):
        """Only return data for current user."""
        return EmailAddress.objects.filter(user=self.request.user)


class EmailActionMixin(CreateAPI):
    """Mixin to modify email addresses for current users."""

    serializer_class = EmptyEmailAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filter queryset for current user."""
        return EmailAddress.objects.filter(
            user=self.request.user, pk=self.kwargs['pk']
        ).first()

    @extend_schema(responses={200: OpenApiResponse(response=EmailAddressSerializer)})
    def post(self, request, *args, **kwargs):
        """Filter item, run action and return data."""
        email = self.get_queryset()
        if not email:
            raise NotFound

        self.special_action(email, request, *args, **kwargs)
        return Response(EmailAddressSerializer(email).data)


class EmailVerifyView(EmailActionMixin):
    """Re-verify an email for a currently logged in user."""

    def special_action(self, email, request, *args, **kwargs):
        """Send confirmation."""
        if email.verified:
            return
        email.send_confirmation(request)


class EmailPrimaryView(EmailActionMixin):
    """Make an email for a currently logged in user primary."""

    def special_action(self, email, *args, **kwargs):
        """Mark email as primary."""
        if email.primary:
            return
        email.set_as_primary()


class EmailRemoveView(EmailActionMixin):
    """Remove an email for a currently logged in user."""

    def special_action(self, email, *args, **kwargs):
        """Delete email."""
        email.delete()

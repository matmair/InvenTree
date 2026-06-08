"""Unit tests for API token generation and authentication."""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import BaseStorage
from django.test import RequestFactory, TestCase

from rest_framework.test import APIClient

from users.admin import ApiTokenAdmin
from users.authentication import ApiTokenAuthentication
from users.models import ApiToken


class ApiTokenTest(TestCase):
    """Tests for the ApiToken model and authentication."""

    def setUp(self):
        """Set up test user and authentication."""
        self.user, _ = User.objects.get_or_create(username='testuser')
        self.auth = ApiTokenAuthentication()

    def test_v1_token(self):
        """Test that v1 tokens can be created and authenticated."""
        key = ApiToken.generate_key()
        ApiToken.objects.create(user=self.user, key=key, version=1)
        user, authenticated_token = self.auth.authenticate_credentials(key)
        self.assertEqual(user, self.user)
        self.assertEqual(authenticated_token.version, 1)

    def test_v2_token(self):
        """Test that v2 tokens can be created and authenticated."""
        key = ApiToken.generate_key()
        token = ApiToken.objects.create(user=self.user, key=key, version=2)
        token.refresh_from_db()
        self.assertEqual(token.key, key[:12])
        user, authenticated_token = self.auth.authenticate_credentials(key)
        self.assertEqual(user, self.user)
        self.assertEqual(authenticated_token.version, 2)

    def test_v2_token_with_peppers(self):
        """Test that v2 tokens can be created and authenticated with peppers."""
        with self.settings(API_TOKEN_PEPPERS={'1': 'pepper1', '2': 'pepper2'}):
            key = ApiToken.generate_key()
            token = ApiToken.objects.create(user=self.user, key=key, version=2)
            self.assertEqual(token.pepper_id, '2')
            user, _ = self.auth.authenticate_credentials(key)
            self.assertEqual(user, self.user)

            with self.settings(
                API_TOKEN_PEPPERS={'1': 'pepper1', '2': 'pepper2', '3': 'pepper3'}
            ):
                user, _ = self.auth.authenticate_credentials(key)
                self.assertEqual(user, self.user)

    def test_api_generates_v2_token(self):
        """Test that the API generates v2 tokens by default."""
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/user/token/', {'name': 'apitest'})
        self.assertEqual(response.status_code, 200)
        token_key = response.data['token']
        token = ApiToken.objects.get(name='apitest', user=self.user)
        self.assertEqual(token.version, 2)
        self.assertEqual(token.key, token_key[:12])
        user, _ = self.auth.authenticate_credentials(token_key)
        self.assertEqual(user, self.user)

    def test_admin_action_disable_v1(self):
        """Test that the admin action to disable v1 tokens works."""
        ApiToken.objects.create(user=self.user, key=ApiToken.generate_key(), version=1)
        ApiToken.objects.create(user=self.user, key=ApiToken.generate_key(), version=2)
        self.assertEqual(ApiToken.objects.filter(version=1, revoked=False).count(), 1)
        admin = ApiTokenAdmin(ApiToken, AdminSite())
        request = RequestFactory().get('/')
        request._messages = BaseStorage(request)
        admin.disable_v1_tokens(request, ApiToken.objects.all())
        self.assertEqual(ApiToken.objects.filter(version=1, revoked=False).count(), 0)
        self.assertEqual(ApiToken.objects.filter(version=2, revoked=False).count(), 1)

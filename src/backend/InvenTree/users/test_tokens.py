import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from users.models import ApiToken
from users.authentication import ApiTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ApiTokenTest(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='testuser')
        self.auth = ApiTokenAuthentication()

    def test_v1_token(self):
        key = ApiToken.generate_key()
        token = ApiToken.objects.create(user=self.user, key=key, version=1)
        user, authenticated_token = self.auth.authenticate_credentials(key)
        self.assertEqual(user, self.user)
        self.assertEqual(authenticated_token.version, 1)

    def test_v2_token(self):
        key = ApiToken.generate_key()
        token = ApiToken.objects.create(user=self.user, key=key, version=2)
        token.refresh_from_db()
        self.assertEqual(token.key, key[:12])
        user, authenticated_token = self.auth.authenticate_credentials(key)
        self.assertEqual(user, self.user)
        self.assertEqual(authenticated_token.version, 2)

    def test_v2_token_with_peppers(self):
        with self.settings(API_TOKEN_PEPPERS={'1': 'pepper1', '2': 'pepper2'}):
            key = ApiToken.generate_key()
            token = ApiToken.objects.create(user=self.user, key=key, version=2)
            self.assertEqual(token.pepper_id, '2')
            user, authenticated_token = self.auth.authenticate_credentials(key)
            self.assertEqual(user, self.user)

            with self.settings(API_TOKEN_PEPPERS={'1': 'pepper1', '2': 'pepper2', '3': 'pepper3'}):
                user, authenticated_token = self.auth.authenticate_credentials(key)
                self.assertEqual(user, self.user)

    def test_api_generates_v2_token(self):
        from rest_framework.test import APIClient
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/user/token/', {'name': 'apitest'})
        self.assertEqual(response.status_code, 200)
        token_key = response.data['token']
        token = ApiToken.objects.get(name='apitest', user=self.user)
        self.assertEqual(token.version, 2)
        self.assertEqual(token.key, token_key[:12])
        user, authenticated_token = self.auth.authenticate_credentials(token_key)
        self.assertEqual(user, self.user)

    def test_admin_action_disable_v1(self):
        from users.admin import ApiTokenAdmin
        from django.contrib.admin.sites import AdminSite
        from django.test import RequestFactory
        from django.contrib.messages.storage.base import BaseStorage
        ApiToken.objects.create(user=self.user, key=ApiToken.generate_key(), version=1)
        ApiToken.objects.create(user=self.user, key=ApiToken.generate_key(), version=2)
        self.assertEqual(ApiToken.objects.filter(version=1, revoked=False).count(), 1)
        admin = ApiTokenAdmin(ApiToken, AdminSite())
        request = RequestFactory().get('/')
        setattr(request, '_messages', BaseStorage(request))
        admin.disable_v1_tokens(request, ApiToken.objects.all())
        self.assertEqual(ApiToken.objects.filter(version=1, revoked=False).count(), 0)
        self.assertEqual(ApiToken.objects.filter(version=2, revoked=False).count(), 1)

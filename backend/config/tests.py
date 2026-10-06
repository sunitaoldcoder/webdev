from django.test import TestCase,override_settings
from django.urls import reverse
from django.conf import settings
class PWAHostingTests(TestCase):
    def test_health_checks_database(self):
        response=self.client.get('/healthz')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['status'],'ok')
    def test_home_serves_build_or_useful_unavailable_state(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200 if (settings.PWA_ROOT/'index.html').exists() else 503)
        self.assertIn('no-cache',response.headers['Cache-Control'])
    @override_settings(SECURE_SSL_REDIRECT=True,SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https'))
    def test_https_redirect_and_trusted_proxy(self):
        self.assertEqual(self.client.get('/').status_code,301)
        self.assertNotEqual(self.client.get('/',HTTP_X_FORWARDED_PROTO='https').status_code,301)
    def test_private_media_is_not_a_public_static_route(self):
        self.assertEqual(self.client.get('/media/diagnoses/private.jpg').status_code,404)

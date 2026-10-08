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

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from farmers.models import Farmer
from crop_diagnosis.models import CropDiagnosis

class MissingDiagnosisImageTests(TestCase):
    def test_missing_image_returns_404_without_exposing_storage_path(self):
        user=get_user_model().objects.create_user(username='9000000001',password='test-password')
        farmer=Farmer.objects.create(user=user,name='Test Farmer',mobile='9000000001',district='Lucknow',village='Pilot Village',language='hi')
        diagnosis=CropDiagnosis.objects.create(farmer=farmer,crop='Wheat',image='diagnoses/missing-test.jpg',result={})
        token=Token.objects.create(user=user)
        response=self.client.get(f'/api/crop-diagnosis/{diagnosis.pk}/image',HTTP_AUTHORIZATION=f'Token {token.key}')
        self.assertEqual(response.status_code,404)
        self.assertNotIn('missing-test.jpg',response.content.decode())
        self.assertTrue(CropDiagnosis.objects.filter(pk=diagnosis.pk).exists())

from io import BytesIO
from PIL import Image
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from farmers.models import Farmer
from farms.models import Crop
from providers.demo import DemoLLM, SampleWeather, SampleMarket
from advisory.models import AdvisoryMessage
from crop_diagnosis.models import CropDiagnosis
import tempfile

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class WorkflowTests(TestCase):
    def setUp(self):
        Crop.objects.create(name='Wheat',name_hi='गेहूँ')
        self.client=APIClient()
        self.registration={'name':'किसान','mobile':'9000000100','password':'SafeTestPass!42','district':'Lucknow','village':'गाँव','language':'hi','crops':['Wheat'],'size_acres':'2.5','irrigation':'canal'}
    def register(self):
        r=self.client.post('/api/auth/register',self.registration,format='json')
        self.assertEqual(r.status_code,201,r.data)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+r.data['data']['token'])
    def test_registration_profile_and_validation(self):
        self.register()
        self.assertEqual(self.client.get('/api/farmers/me').data['data']['profile']['language'],'hi')
        self.assertEqual(self.client.get('/api/farms').data['data'][0]['crops'][0]['name'],'Wheat')
        r=self.client.post('/api/auth/register',self.registration,format='json')
        self.assertEqual(r.status_code,400)
    def test_unauthenticated_private_endpoints(self):
        for path in ['farmers/me','farms','admin/analytics','expert-cases']:
            self.assertEqual(self.client.get('/api/'+path).status_code,401)
    def test_advisory_safety_feedback_and_ownership(self):
        self.register()
        r=self.client.post('/api/advisory/ask',{'question':'गेहूँ के पीले पत्ते में दवा कितनी दूँ?'},format='json')
        self.assertEqual(r.status_code,200)
        self.assertTrue(r.data['data']['expert_required'])
        self.assertEqual(r.data['data']['confidence'],'low')
        self.assertNotIn('ml',r.data['data']['answer'])
        mid=r.data['data']['message_id']
        self.assertEqual(self.client.post('/api/feedback',{'message_id':mid,'helpful':False,'comment':'More details'},format='json').status_code,201)
        other=User.objects.create_user('other',password='anotherSafePass!')
        Farmer.objects.create(user=other,mobile='9000000101',name='Other',district='Varanasi',village='Demo')
        self.client.force_authenticate(other)
        self.assertEqual(self.client.post('/api/feedback',{'message_id':mid,'helpful':True},format='json').status_code,404)
        self.assertEqual(self.client.get('/api/farmers/me').data['data']['questions'],[])
    def test_image_validation_and_low_confidence(self):
        self.register()
        invalid=SimpleUploadedFile('bad.jpg',b'not an image',content_type='image/jpeg')
        self.assertEqual(self.client.post('/api/crop-diagnosis',{'image':invalid,'crop':'Wheat'},format='multipart').status_code,400)
        stream=BytesIO();Image.new('RGB',(80,80),'green').save(stream,format='JPEG')
        image=SimpleUploadedFile('crop.jpg',stream.getvalue(),content_type='image/jpeg')
        r=self.client.post('/api/crop-diagnosis',{'image':image,'crop':'Wheat'},format='multipart')
        self.assertEqual(r.status_code,201,r.data)
        self.assertTrue(r.data['data']['expert_required'])
        self.assertTrue(r.data['data']['is_demo'])
        self.assertEqual(CropDiagnosis.objects.count(),1)
    def test_weather_market_are_explicit_samples(self):
        self.register()
        weather=self.client.get('/api/weather').data['data']
        self.assertTrue(weather['is_sample']);self.assertEqual(len(weather['forecast']),5)
        market=self.client.get('/api/market-prices').data['data']
        self.assertEqual(market['live_status'],'Current market price data is unavailable.')
        self.assertTrue(market['prices'][0]['is_sample'])
        self.assertEqual(self.client.get('/api/weather?district=Unknown').status_code,400)
    def test_expert_and_admin_permissions(self):
        self.register()
        r=self.client.post('/api/expert-cases',{'question':'मदद चाहिए'},format='json')
        self.assertEqual(r.status_code,201)
        self.assertEqual(self.client.get('/api/admin/analytics').status_code,403)
        self.assertEqual(self.client.post(f"/api/expert-cases/{r.data['data']['id']}/respond",{'text':'test'},format='json').status_code,403)
        staff=User.objects.create_user('expert',password='safePass!456',is_staff=True)
        self.client.force_authenticate(staff)
        self.assertEqual(self.client.get('/api/admin/analytics').status_code,200)
        self.assertEqual(self.client.post(f"/api/expert-cases/{r.data['data']['id']}/respond",{'text':'Please consult local KVK','resolved':True},format='json').status_code,200)
    def test_disabled_whatsapp_and_logout(self):
        self.assertEqual(self.client.post('/api/whatsapp/webhook',{},format='json').status_code,503)
        self.register();self.assertEqual(self.client.post('/api/auth/logout').status_code,200)
        self.assertEqual(self.client.get('/api/farmers/me').status_code,401)

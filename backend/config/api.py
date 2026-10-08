from django.contrib.auth import authenticate
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.authtoken.models import Token
from accounts.serializers import RegistrationSerializer, FarmerSerializer
from accounts.services import AccountService
from farms.services import FarmService
from experts.services import ExpertService
from analytics.services import AnalyticsService
from farmers.models import Farmer, DISTRICTS
from farms.models import Farm, Crop
from advisory.models import AdvisoryMessage
from advisory.services import AdvisoryService
from crop_diagnosis.models import CropDiagnosis
from crop_diagnosis.services import DiagnosisService
from experts.models import ExpertCase, ExpertResponse
from feedback.models import Feedback
from subscriptions.models import Subscription
from providers.factory import weather_provider, market_provider
from providers.weather import WeatherUnavailable

def ok(data, status=200):
    return Response({'data':data},status=status)
def farmer(request):
    return get_object_or_404(Farmer,user=request.user)
def text(request, key, max_length=2000):
    value = request.data.get(key,'')
    if not isinstance(value,str) or not value.strip() or len(value)>max_length:
        raise ValidationError({key:'Required text, within length limit'})
    return value.strip()
def object_id(request,key):
    return serializers.IntegerField(min_value=1).run_validation(request.data.get(key))
def optional_text(request, key, max_length=2000):
    value=request.data.get(key,'')
    if not isinstance(value,str) or len(value)>max_length:
        raise ValidationError({key:'Invalid text or length'})
    return value
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data
    f,token=AccountService.register(d)
    return ok({'token':token.key,'farmer':FarmerSerializer(f).data},201)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(username=request.data.get('mobile'),password=request.data.get('password'))
    if not user:
        return Response({'error':'Invalid mobile or password'},status=401)
    return ok({'token':Token.objects.get_or_create(user=user)[0].key,'is_staff':user.is_staff})
@api_view(['POST'])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return ok({'logged_out':True})
@api_view(['GET','PATCH'])
def me(request):
    f=farmer(request)
    if request.method=='PATCH':
        s=FarmerSerializer(f,data=request.data,partial=True);s.is_valid(raise_exception=True);s.save()
    return ok({'profile':FarmerSerializer(f).data,'questions':list(AdvisoryMessage.objects.filter(conversation__farmer=f).order_by('-id').values('id','question','answer','created_at')[:10]),'diagnoses':list(CropDiagnosis.objects.filter(farmer=f).order_by('-id').values('id','crop','result','created_at')[:10]),'weather_alerts':list(f.weatheralert_set.values('text','created_at')),'saved_prices':list(f.marketprice_set.values()),'subscription':Subscription.objects.filter(farmer=f).values_list('status',flat=True).first() or 'free'})
@api_view(['GET','POST','PATCH'])
def farms(request):
    f=farmer(request)
    if request.method in ['POST','PATCH']:
        FarmService.save(f,request.data,request.method=='PATCH')
    return ok([{'id':x.id,'size_acres':str(x.size_acres),'irrigation':x.irrigation,'crops':list(x.crops.values('name','name_hi'))} for x in Farm.objects.filter(farmer=f)])
@api_view(['POST'])
def ask(request):
    return ok(AdvisoryService().ask(farmer(request),text(request,'question')))
@api_view(['POST'])
def diagnosis(request):
    image=request.FILES.get('image')
    if not image: raise ValidationError({'image':'Image required'})
    crop=text(request,'crop',50)
    if not Crop.objects.filter(name=crop).exists(): raise ValidationError('Unknown crop')
    return ok(DiagnosisService().diagnose(farmer(request),image,crop,optional_text(request,'description')),201)
@api_view(['GET'])
def weather(request):
    district=request.query_params.get('district',farmer(request).district)
    if district not in DISTRICTS: raise ValidationError('Unknown district')
    try:
        return ok(weather_provider().get(district))
    except WeatherUnavailable as exc:
        return Response({'error':str(exc)},status=503)
@api_view(['GET','POST'])
def market(request):
    f=farmer(request)
    crop=request.query_params.get('crop','Wheat');district=request.query_params.get('district',f.district)
    if district not in DISTRICTS or not Crop.objects.filter(name=crop).exists(): raise ValidationError('Invalid district or crop')
    data=market_provider().get(crop,district,request.query_params.get('market',''))
    if request.method=='POST':
        from market_prices.models import MarketPrice
        p=data['prices'][0];MarketPrice.objects.create(farmer=f,**{k:p[k] for k in ['commodity','district','market','minimum','maximum','modal','date','source','is_sample']})
    return ok(data)
@api_view(['POST'])
def feedback(request):
    message=get_object_or_404(AdvisoryMessage,pk=object_id(request,'message_id'),conversation__farmer=farmer(request))
    helpful=request.data.get('helpful')
    if not isinstance(helpful,bool): raise ValidationError('helpful must be boolean')
    Feedback.objects.update_or_create(farmer=farmer(request),message=message,defaults={'helpful':helpful,'comment':optional_text(request,'comment')})
    return ok({'saved':True},201)
@api_view(['GET','POST'])
def cases(request):
    if request.method=='POST':
        f=farmer(request);diag=None
        if request.data.get('diagnosis_id'): diag=get_object_or_404(CropDiagnosis,pk=object_id(request,'diagnosis_id'),farmer=f)
        c=ExpertService.create(f,text(request,'question'),optional_text(request,'ai_suggestion',4000),diag)
        return ok({'id':c.id,'status':'pending','notice':'Demo queue: no expert response time is guaranteed.'},201)
    qs=ExpertCase.objects.all() if request.user.is_staff else ExpertCase.objects.filter(farmer=farmer(request))
    return ok([{'id':c.id,'farmer':c.farmer.name,'question':c.question,'ai_suggestion':c.ai_suggestion,'diagnosis_id':c.diagnosis_id,'resolved':c.resolved,'responses':list(c.responses.values('text','created_at'))} for c in qs.order_by('-id')])
@api_view(['POST'])
@permission_classes([IsAdminUser])
def respond(request,pk):
    c=get_object_or_404(ExpertCase,pk=pk)
    ExpertService.respond(c,request.user,text(request,'text'),request.data.get('resolved') is True)
    return ok({'resolved':c.resolved})
@api_view(['GET'])
def diagnosis_image(request,pk):
    d=get_object_or_404(CropDiagnosis,pk=pk)
    if not request.user.is_staff and d.farmer.user_id!=request.user.id: raise PermissionDenied()
    try:
        image_file = d.image.open('rb')
    except (FileNotFoundError, OSError, ValueError):
        return Response({'error':'The uploaded crop photo is no longer available. Please upload a new photo.'},status=404)
    return FileResponse(image_file,content_type='application/octet-stream')
@api_view(['GET'])
@permission_classes([IsAdminUser])
def analytics(request):
    return ok(AnalyticsService.summary())
@api_view(['POST'])
@permission_classes([AllowAny])
def whatsapp(request):
    return Response({'error':'WhatsApp integration is disabled; no messages processed.'},status=503)

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from farmers.models import Farmer, DISTRICTS
from farms.models import Crop, Farm
from subscriptions.models import Subscription
class Command(BaseCommand):
    help = 'Seed sample farmers; requires DEMO_PASSWORD, never sets production admin credentials.'
    def add_arguments(self,parser):
        parser.add_argument('--with-admin',action='store_true',help='Create explicit local demo staff account')
    @transaction.atomic
    def handle(self,*args,**kwargs):
        password=os.environ.get('DEMO_PASSWORD')
        if not password: raise RuntimeError('Set DEMO_PASSWORD to seed demo accounts')
        for name,hi in [('Wheat','गेहूँ'),('Rice/Paddy','धान'),('Mustard','सरसों'),('Potato','आलू'),('Tomato','टमाटर'),('Pulses','दालें')]:
            Crop.objects.get_or_create(name=name,defaults={'name_hi':hi})
        for i,district in enumerate(DISTRICTS):
            mobile=f'900000000{i}'
            user,created=User.objects.get_or_create(username=mobile)
            if created:user.set_password(password);user.save()
            f,_=Farmer.objects.get_or_create(user=user,defaults={'mobile':mobile,'name':['शिवम','सुनीता','राम','गीता'][i],'district':district,'village':'नमूना गाँव'})
            farm,created=Farm.objects.get_or_create(farmer=f,defaults={'size_acres':2.5,'irrigation':'canal'})
            if created:farm.crops.set(Crop.objects.filter(name__in=['Wheat','Rice/Paddy']))
            Subscription.objects.get_or_create(farmer=f)
        if kwargs.get('with_admin'):
            admin,created=User.objects.get_or_create(username='9000000099',defaults={'is_staff':True,'is_superuser':True})
            if created: admin.set_password(password);admin.save()
        self.stdout.write('Seeded four demo farmers and six crops; admin is opt-in via --with-admin.')

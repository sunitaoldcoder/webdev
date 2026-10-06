"""Atomic farmer registration; password hashes are managed by Django."""
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from farmers.models import Farmer
from farms.models import Crop, Farm
from subscriptions.models import Subscription
class AccountService:
    @staticmethod
    def register(data: dict):
        try:
            with transaction.atomic():
                user=User.objects.create_user(username=data['mobile'],password=data['password'])
                farmer=Farmer.objects.create(user=user,**{key:data[key] for key in ['name','mobile','district','village','language']})
                farm=Farm.objects.create(farmer=farmer,size_acres=data['size_acres'],irrigation=data['irrigation'])
                farm.crops.set(Crop.objects.filter(name__in=data['crops']))
                Subscription.objects.create(farmer=farmer)
                token=Token.objects.create(user=user)
                return farmer,token
        except IntegrityError as exc:
            raise ValidationError({'mobile':'Mobile already registered'}) from exc

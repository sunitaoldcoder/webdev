from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from accounts.serializers import RegistrationSerializer
from .models import Farm, Crop
class FarmService:
    @staticmethod
    @transaction.atomic
    def save(farmer, data: dict, update: bool=False):
        serializer=RegistrationSerializer()
        values={key:serializer.fields[key].run_validation(data.get(key)) for key in ['size_acres','irrigation','crops']}
        serializer.validate_crops(values['crops'])
        farm=get_object_or_404(Farm,pk=serializers.IntegerField(min_value=1).run_validation(data.get('id')),farmer=farmer) if update else Farm(farmer=farmer)
        farm.size_acres=values['size_acres'];farm.irrigation=values['irrigation'];farm.save()
        farm.crops.set(Crop.objects.filter(name__in=values['crops']))
        return farm

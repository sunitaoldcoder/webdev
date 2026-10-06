"""Seed the crop catalogue without creating demo users or passwords."""
from django.core.management.base import BaseCommand
from farms.models import Crop
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        for en,hi in [('Wheat','गेहूँ'),('Rice/Paddy','धान'),('Mustard','सरसों'),('Potato','आलू'),('Tomato','टमाटर'),('Pulses','दालें')]:
            Crop.objects.get_or_create(name=en,defaults={'name_hi':hi})
        self.stdout.write('Crop catalogue ready; no user accounts created.')

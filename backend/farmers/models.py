from django.db import models
from django.contrib.auth.models import User
from common import Timestamped
DISTRICTS = ['Lucknow','Rae Bareli','Gorakhpur','Varanasi']
class Farmer(Timestamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    district = models.CharField(max_length=30, choices=[(d,d) for d in DISTRICTS])
    village = models.CharField(max_length=100)
    language = models.CharField(max_length=10, default='hi', choices=[('hi','Hindi'),('en','English')])

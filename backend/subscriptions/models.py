from django.db import models
from common import Timestamped
class Subscription(Timestamped):
    farmer = models.OneToOneField('farmers.Farmer',on_delete=models.CASCADE)
    status = models.CharField(max_length=20,default='free')

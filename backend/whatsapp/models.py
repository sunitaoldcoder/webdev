from django.db import models
from common import Timestamped
class WhatsAppMessage(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer',null=True,on_delete=models.SET_NULL)
    external_id = models.CharField(max_length=100,unique=True)
    kind = models.CharField(max_length=20)
    status = models.CharField(max_length=20,default='received')

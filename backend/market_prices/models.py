from django.db import models
from common import Timestamped
class MarketPrice(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE, null=True)
    commodity = models.CharField(max_length=50)
    district = models.CharField(max_length=30)
    market = models.CharField(max_length=100)
    minimum = models.DecimalField(max_digits=10,decimal_places=2)
    maximum = models.DecimalField(max_digits=10,decimal_places=2)
    modal = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    date = models.DateField()
    source = models.CharField(max_length=100)
    is_sample = models.BooleanField(default=True)

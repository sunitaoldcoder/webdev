from django.db import models
from common import Timestamped
class Crop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_hi = models.CharField(max_length=50)
class Farm(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE)
    size_acres = models.DecimalField(max_digits=8, decimal_places=2)
    irrigation = models.CharField(max_length=40)
    crops = models.ManyToManyField(Crop, through='FarmerCrop')
class FarmerCrop(Timestamped):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['farm','crop'],name='unique_farm_crop')]

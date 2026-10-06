from django.db import models
from common import Timestamped
class CropDiagnosis(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diagnoses/')
    crop = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    result = models.JSONField(default=dict)

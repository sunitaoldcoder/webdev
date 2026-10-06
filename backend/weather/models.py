from django.db import models
from common import Timestamped
class WeatherAlert(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE)
    text = models.TextField()

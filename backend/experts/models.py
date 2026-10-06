from django.db import models
from common import Timestamped
class ExpertCase(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer',on_delete=models.CASCADE)
    question = models.TextField()
    ai_suggestion = models.TextField(blank=True)
    diagnosis = models.ForeignKey('crop_diagnosis.CropDiagnosis',null=True,blank=True,on_delete=models.SET_NULL)
    resolved = models.BooleanField(default=False)
class ExpertResponse(Timestamped):
    case = models.ForeignKey(ExpertCase,on_delete=models.CASCADE,related_name='responses')
    expert = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    text = models.TextField()

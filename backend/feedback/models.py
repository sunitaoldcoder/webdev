from django.db import models
from common import Timestamped
class Feedback(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer',on_delete=models.CASCADE)
    message = models.ForeignKey('advisory.AdvisoryMessage',on_delete=models.CASCADE)
    helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['farmer','message'],name='unique_farmer_message_feedback')]

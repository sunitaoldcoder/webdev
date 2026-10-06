from django.db import models
from common import Timestamped
class AdvisoryConversation(Timestamped):
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE)
class AdvisoryMessage(Timestamped):
    conversation = models.ForeignKey(AdvisoryConversation, on_delete=models.CASCADE, related_name='messages')
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=40)
    context = models.JSONField(default=dict)

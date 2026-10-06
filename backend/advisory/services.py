from providers.factory import llm_provider
from .models import AdvisoryConversation, AdvisoryMessage
class AdvisoryService:
    def __init__(self, provider=None):
        self.provider = provider or llm_provider()
    def ask(self, farmer, question: str) -> dict:
        crops = list(farmer.farm_set.values_list('crops__name',flat=True))
        context = {'district':farmer.district,'language':farmer.language,'crops':crops,'season':'local season requires verification','weather_status':'sample_only'}
        result = self.provider.answer(question, context)
        conversation = AdvisoryConversation.objects.create(farmer=farmer)
        message = AdvisoryMessage.objects.create(conversation=conversation,question=question,answer=result['answer'],category=result['category'],context=context)
        return dict(result, message_id=message.id)

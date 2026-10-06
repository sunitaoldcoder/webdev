from collections import Counter
from farmers.models import Farmer
from farms.models import Farm
from advisory.models import AdvisoryMessage
from crop_diagnosis.models import CropDiagnosis
from experts.models import ExpertCase
from feedback.models import Feedback
from subscriptions.models import Subscription
class AnalyticsService:
    @staticmethod
    def summary() -> dict:
        return {'farmers':Farmer.objects.count(),'questions':AdvisoryMessage.objects.count(),'diagnoses':CropDiagnosis.objects.count(),'escalations':ExpertCase.objects.count(),'districts':dict(Counter(Farmer.objects.values_list('district',flat=True))),'crops':dict(Counter(Farm.objects.values_list('crops__name',flat=True))),'common_problems':dict(Counter(AdvisoryMessage.objects.values_list('category',flat=True))),'frequent_questions':Counter(AdvisoryMessage.objects.values_list('question',flat=True)).most_common(5),'feedback':list(Feedback.objects.values('helpful','comment')),'subscriptions':dict(Counter(Subscription.objects.values_list('status',flat=True)))}

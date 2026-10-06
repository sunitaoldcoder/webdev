from django.db import transaction
from .models import ExpertCase, ExpertResponse
class ExpertService:
    @staticmethod
    def create(farmer, question: str, suggestion: str='', diagnosis=None):
        return ExpertCase.objects.create(farmer=farmer,question=question,ai_suggestion=suggestion,diagnosis=diagnosis)
    @staticmethod
    @transaction.atomic
    def respond(case, expert, text: str, resolved: bool=False):
        ExpertResponse.objects.create(case=case,expert=expert,text=text)
        case.resolved=resolved;case.save()
        return case

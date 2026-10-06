"""Channel-neutral routing seam for a future verified WhatsApp webhook."""
from typing import Protocol
from advisory.services import AdvisoryService
class WhatsAppTransport(Protocol):
    def send_text(self, mobile: str, text: str) -> None: ...
class MessageRouter:
    def __init__(self, advisory=None):
        self.advisory=advisory or AdvisoryService()
    def route(self, farmer, kind: str, content: str) -> dict:
        if kind=='text':
            return self.advisory.ask(farmer,content)
        return {'status':'unsupported','answer':'कृपया अभी text में सवाल भेजें।'}
# Activation requires signature verification, webhook challenge handling,
# replay protection, opt-in policy and an authenticated transport adapter.

from datetime import date, timedelta
from django.utils.timezone import now
DISCLAIMER = 'AI-based advisory. Verify important crop-treatment decisions with a qualified agriculture expert/KVK.'
class DemoLLM:
    def answer(self, question: str, context: dict) -> dict:
        high_risk = any(x in question.lower() for x in ['dose','fertil','pestic','yellow','disease','कीटनाशक','खाद','पीले','रोग','दवा','बेच','sell','grow','उगाऊँ'])
        text = 'यह सामान्य शैक्षिक जानकारी है। मिट्टी, फसल की अवस्था और स्थानीय स्थिति देखकर निर्णय लें। अपने खेत की अधिक जानकारी बताएं।'
        if high_risk:
            text = 'इस प्रश्न में फसल या आर्थिक जोखिम हो सकता है। बिना जाँच के कारण या दवा की मात्रा तय नहीं की जा सकती। प्रभावित पौधे की तस्वीर लें और स्थानीय KVK या कृषि विशेषज्ञ से सलाह लें।'
        if 'rain' in question.lower() or 'बारिश' in question or 'मौसम' in question:
            text = 'वास्तविक मौसम उपलब्ध होने पर ही सिंचाई का निर्णय लें। मौसम पेज पर अभी केवल नमूना डेटा है।'
        if 'price' in question.lower() or 'भाव' in question or 'mandi' in question.lower():
            text = 'Current market price data is unavailable. मंडी पेज पर केवल नमूना भाव हैं; बिक्री से पहले मंडी से पुष्टि करें।'
        if context.get('language') == 'en':
            text = 'Demo educational guidance: consider soil, crop stage and local conditions. No verified treatment or dose is available. Consult a qualified agriculture expert/KVK for crop or financial risk. Live weather and market prices are unavailable; sample data is shown in their modules.'
        return {'answer':text,'category':'expert_required' if high_risk else 'general_education','confidence':'low','expert_required':high_risk,'is_demo':True,'sources':[],'disclaimer':DISCLAIMER}
class DemoVision:
    def analyze(self, image: bytes, crop: str, description: str) -> dict:
        return {'possible_issue':'तस्वीर से विश्वसनीय पहचान उपलब्ध नहीं है','confidence':'low','symptoms':['पत्तियों का रंग, धब्बे और कीट विशेषज्ञ को दिखाएँ'],'next_steps':['प्रभावित और स्वस्थ पौधों की स्पष्ट तस्वीर लें','KVK / कृषि विशेषज्ञ से जाँच करवाएँ','बिना पुष्टि दवा या खाद की मात्रा न बदलें'],'expert_required':True,'is_demo':True,'disclaimer':DISCLAIMER}
class SampleWeather:
    def get(self, district: str) -> dict:
        return {'district':district,'temperature':29,'rain_probability':65,'humidity':74,'wind_kmh':11,'forecast':[{'date':str(date.today()+timedelta(days=i)),'temperature':29+i%3,'rain_probability':[65,80,35,20,45][i]} for i in range(5)],'source':'Development sample — not live weather','is_sample':True,'updated_at':now().isoformat(),'advisory':'नमूना: बारिश की संभावना अधिक होने पर सिंचाई टालने पर विचार करें। वास्तविक पूर्वानुमान की पुष्टि करें।'}
class SampleMarket:
    def get(self, crop: str, district: str, market: str) -> dict:
        return {'is_sample':True,'live_status':'Current market price data is unavailable.','prices':[{'commodity':crop or 'Wheat','district':district,'market':market or district+' Mandi','minimum':2200,'maximum':2450,'modal':2320,'unit':'INR/quintal','date':str(date.today()),'source':'Development sample — not official prices','updated_at':now().isoformat(),'is_sample':True}]}

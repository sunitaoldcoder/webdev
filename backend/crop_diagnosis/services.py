from PIL import Image, UnidentifiedImageError
from rest_framework.exceptions import ValidationError
from providers.factory import vision_provider
from .models import CropDiagnosis
class DiagnosisService:
    def __init__(self, provider=None):
        self.provider = provider or vision_provider()
    def diagnose(self, farmer, image, crop: str, description: str):
        if image.size > 5*1024*1024:
            raise ValidationError('Image must be under 5 MB')
        try:
            with Image.open(image) as photo:
                if photo.format not in ['JPEG','PNG','WEBP'] or photo.width*photo.height > 20000000:
                    raise ValidationError('Use JPEG, PNG or WEBP under 20 megapixels')
                photo.verify()
        except (UnidentifiedImageError,OSError,Image.DecompressionBombError):
            raise ValidationError('Invalid image')
        image.seek(0)
        result = self.provider.analyze(image.read(),crop,description)
        image.seek(0)
        diagnosis = CropDiagnosis.objects.create(farmer=farmer,image=image,crop=crop,description=description,result=result)
        return dict(result,id=diagnosis.id)

from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from farmers.models import DISTRICTS, Farmer
from farms.models import Crop
class RegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    mobile = serializers.RegexField(r'^[6-9][0-9]{9}$')
    password = serializers.CharField(write_only=True,validators=[validate_password])
    district = serializers.ChoiceField(choices=DISTRICTS)
    village = serializers.CharField(max_length=100)
    language = serializers.ChoiceField(choices=['hi','en'],default='hi')
    crops = serializers.ListField(child=serializers.CharField(),allow_empty=False)
    size_acres = serializers.DecimalField(max_digits=8,decimal_places=2,min_value=Decimal("0.01"))
    irrigation = serializers.ChoiceField(choices=['rainfed','canal','borewell','drip','other'])
    def validate_crops(self, value):
        if set(value)-set(Crop.objects.values_list('name',flat=True)):
            raise serializers.ValidationError('Unknown crop')
        return value
    def validate_mobile(self,value):
        if Farmer.objects.filter(mobile=value).exists():
            raise serializers.ValidationError('Mobile already registered')
        return value
class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['id','name','mobile','district','village','language']
        read_only_fields = ['id','mobile']

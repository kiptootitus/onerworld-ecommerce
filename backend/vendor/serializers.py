# serializers.py

from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorUpdateSerializer(serializers.Serializer):
    country_of_citizenship = serializers.CharField(max_length=500, required=False)
    country_of_birth = serializers.CharField(max_length=500, required=False)
    date_of_birth = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False)
    proof_of_identity = serializers.CharField(max_length=100, required=False)
    identity_number = serializers.CharField(max_length=500, required=False)
    identity_upload = serializers.FileField(required=False)
    date_of_expiry = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y'], required=False)
    country_of_issue = serializers.CharField(max_length=500, required=False)
    phone_number = serializers.CharField(max_length=20, required=False)
    created_by = serializers.CharField(max_length=100, required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

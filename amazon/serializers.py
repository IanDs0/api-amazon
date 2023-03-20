from rest_framework import serializers

from .models import Asin

class AsinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asin
        exclude = ['id']
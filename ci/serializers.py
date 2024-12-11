from .models import Name
from rest_framework import serializers

class nameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = '__all__'
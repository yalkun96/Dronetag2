from rest_framework import serializers
from .models import *


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryMessage
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusMessage
        fields = '__all__'

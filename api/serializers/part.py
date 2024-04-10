from api.model.part import Part
from datetime import datetime, timedelta, timezone
from rest_framework import serializers


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('__all__')
        read_only_fields = ('id',)
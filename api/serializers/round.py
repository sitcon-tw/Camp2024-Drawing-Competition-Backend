from api.models import Round
from rest_framework import serializers


class RoundGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = "__all__"
        read_only_fields = ("id",)
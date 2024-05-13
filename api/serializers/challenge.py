from api.models import Challenge
from rest_framework import serializers


class ChallengeGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"
        read_only_fields = ("id",)
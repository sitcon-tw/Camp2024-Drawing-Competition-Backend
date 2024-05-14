from api.models import Challenge
from rest_framework import serializers


class ChallengeGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"
        read_only_fields = ("id",)


class ChallengeTeamSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
    description = serializers.CharField()
    round_id = serializers.IntegerField()
    is_valid = serializers.BooleanField()

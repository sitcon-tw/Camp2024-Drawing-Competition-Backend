from api.models import Challenge
from rest_framework import serializers


class ChallengeGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = "__all__"
        read_only_fields = ("id",)

# Response DTO 列出隊伍中所有挑戰解題狀態
class ChallengeTeamSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    round_id = serializers.IntegerField()
    is_valid = serializers.BooleanField()

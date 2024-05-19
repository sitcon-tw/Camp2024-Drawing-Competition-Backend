from api.models import Round
from rest_framework import serializers
from api.serializers.challenge import ChallengeGeneralSerializer


class RoundGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = "__all__"
        read_only_fields = ("id",)


class RoundChallengeSerializer(serializers.ModelSerializer):
    challenge_list = ChallengeGeneralSerializer(
        source="challenge_set", many=True, read_only=True
    )

    class Meta:
        model = Round
        fields = "__all__"
        read_only_fields = ("id",)

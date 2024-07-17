from api.models import Submission, Team, Challenge, Round
from rest_framework import serializers
from django.utils import timezone


class SubmissionGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ("id",)


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id", "code", "team", "challenge")
        read_only_fields = ("id",)

    def create(self, validated_data):
        round_instance = Challenge.objects.get(
            id=validated_data["challenge"].id
        ).round_id
        return Submission.objects.create(
            code=validated_data["code"],
            status="doing",
            team=validated_data["team"],
            round=round_instance,
            challenge=validated_data["challenge"],
        )
class SubmissonSubmitResponseSeriallizer(serializers.ModelSerializer):
    draw_image_url = serializers.CharField(allow_null=True)
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ("id",)
    
    def create(self, validated_data):
        round_instance = Challenge.objects.get(
            id=validated_data["challenge"].id
        ).round_id
        return Submission.objects.create(
            code=validated_data["code"],
            status="doing",
            team=validated_data["team"],
            round=round_instance,
            challenge=validated_data["challenge"],
        )
    
class StoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    fitness = serializers.IntegerField()
    word_count = serializers.IntegerField()
    execution_time = serializers.IntegerField()
    stdout = serializers.CharField()
    stderr = serializers.CharField()
    status = serializers.CharField()
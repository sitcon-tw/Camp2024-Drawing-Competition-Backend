from api.models import Round
from rest_framework import serializers
from api.serializers.submission import SubmissionGeneralSerializer


class StatisticTeamChallengeFitnessSerializer(serializers.Serializer):
    challenge = serializers.IntegerField()
    max_fitness = serializers.IntegerField()
    submission = SubmissionGeneralSerializer()


class StatisticTeamChallengeSubmissionSerializer(serializers.Serializer):
    challenge = serializers.IntegerField()
    submission_count = serializers.IntegerField()

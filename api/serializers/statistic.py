from api.models import Round
from rest_framework import serializers
from api.serializers.submission import SubmissionGeneralSerializer


# Response DTO 統計單一隊伍所有挑戰最高分
class StatisticTeamChallengeScoreResponseDTO(serializers.Serializer):
    challenge = serializers.IntegerField()
    max_score = serializers.IntegerField()
    submission = SubmissionGeneralSerializer()


# Response DTO 統計單一隊伍所有挑戰提交次數
class StatisticTeamChallengeSubmissionCountResponseDTO(serializers.Serializer):
    challenge = serializers.IntegerField()
    submission_count = serializers.IntegerField()


# Response DTO 統計單一隊伍在單一回合的總分
class StatisticTeamRoundTotalScoreResponseDTO(serializers.Serializer):
    round_id = serializers.IntegerField()
    team_id = serializers.IntegerField()
    total_score = serializers.IntegerField()


# Response DTO 統計所有隊伍在單一回合的總分
class StatisticAllTeamSingleRoundTotalScoreResponseDTO(serializers.Serializer):
    team_id = serializers.IntegerField()
    team_name = serializers.CharField()
    total_score = serializers.IntegerField()
    score_list = serializers.ListField(child=serializers.IntegerField())


# Response DTO 統計所有隊伍在所有回合的總分
class StatisticAllTeamRoundTotalScoreResponseDTO(serializers.Serializer):
    team_id = serializers.IntegerField()
    team_name = serializers.CharField()
    round_id_list = serializers.ListField(child=serializers.IntegerField())
    total_score_list = serializers.ListField(child=serializers.IntegerField())


# Response DTO 統計該挑戰前三高分隊伍
class StatisticTop3TeamChallengeScoreResponseDTO(serializers.Serializer):
    team = serializers.IntegerField()
    team_name = serializers.CharField()
    max_score = serializers.IntegerField()
    fitness = serializers.IntegerField()
    execution_time = serializers.CharField()

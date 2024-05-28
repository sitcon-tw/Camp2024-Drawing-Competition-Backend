from django.urls import path
from api.views.statistic import (
    StatisticAllTeamRoundTotalScoreAPIView,
    StatisticAllTeamSingleRoundTotalScoreAPIView,
    TeamChallengeScoreStaticAPIView,
    TeamChallengeSubmissionStaticAPIView,
    TeamRoundScoreStatisticAPIView,
    StatisticTop3TeamChallengeScore,
)

urlpatterns = [
    # Statistic Routes
    # 統計該隊伍各挑戰最高分
    path(
        "team/",
        TeamChallengeScoreStaticAPIView.as_view(),
        name="statistic-team",
    ),
    # 統計該隊伍各挑戰提交答案次數
    path(
        "submission/",
        TeamChallengeSubmissionStaticAPIView.as_view(),
        name="statistic-submission",
    ),
    # 統計指定回合指定隊伍分數
    path(
        "round/<int:round_id>/team/",
        TeamRoundScoreStatisticAPIView.as_view(),
        name="statistic-round-team",
    ),
    # 統計當前回合所有隊伍總分
    path(
        "round/allTeam/",
        StatisticAllTeamRoundTotalScoreAPIView.as_view(),
        name="statistic-round-allTeam",
    ),
    # 統計單回合所有挑戰各隊伍分數
    path(
        "round/<int:round_id>/allTeam/",
        StatisticAllTeamSingleRoundTotalScoreAPIView.as_view(),
        name="statistic-single-round-allTeam",
    ),
    # 統計挑戰賽前三名
    path(
        "challenge/<int:challenge_id>/top3Team/",
        StatisticTop3TeamChallengeScore.as_view(),
        name="statistic-challenge-top3-team",
    ),
]

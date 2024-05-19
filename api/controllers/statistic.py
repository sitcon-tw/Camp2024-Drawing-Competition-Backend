from django.urls import path
from api.views.statistic import (
    StatisticAllTeamRoundTotalScoreAPIView,
    StatisticAllTeamSingleRoundTotalScoreAPIView,
    TeamChallengeScoreStaticAPIView,
    TeamChallengeSubmissionStaticAPIView,
    TeamRoundScoreStatisticAPIView,
)

urlpatterns = [
    # Statistic Routes
    path(
        "team/",
        TeamChallengeScoreStaticAPIView.as_view(),
        name="statistic-team",
    ),
    path(
        "submission/",
        TeamChallengeSubmissionStaticAPIView.as_view(),
        name="statistic-submission",
    ),
    path(
        "round/<int:round_id>/team/",
        TeamRoundScoreStatisticAPIView.as_view(),
        name="statistic-round-team",
    ),
    path(
        "round/allTeam/",
        StatisticAllTeamRoundTotalScoreAPIView.as_view(),
        name="statistic-round-allTeam",
    ),
    path(
        "round/<int:round_id>/allTeam/",
        StatisticAllTeamSingleRoundTotalScoreAPIView.as_view(),
        name="statistic-single-round-allTeam",
    ),
]

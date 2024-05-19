from django.urls import path

from api.views.challenge import (
    ChallengeAPIView,
    ChallengeRetrieveAPIView,
    ChallengeTeamListAPIView,
)

urlpatterns = [
    # Challenge Routes
    path("", ChallengeAPIView.as_view(), name="challenge"),
    path(
        "<int:challenge_id>/",
        ChallengeRetrieveAPIView.as_view(),
        name="challenge-operate",
    ),
    path("team/", ChallengeTeamListAPIView.as_view(), name="challenge-team"),
]

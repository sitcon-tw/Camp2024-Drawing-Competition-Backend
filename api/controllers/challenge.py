from django.urls import path

from api.views.challenge import (
    ChallengeAPIView,
    ChallengeRetrieveSingleAPIView,
    ChallengeTeamListAPIView,
)

urlpatterns = [
    # Challenge Routes
    path("", ChallengeAPIView.as_view(), name="challenge"),
    path(
        "<int:id>/",
        ChallengeRetrieveSingleAPIView.as_view(),
        name="challenge-single-operate",
    ),
    path("team/", ChallengeTeamListAPIView.as_view(), name="challenge-team"),
]

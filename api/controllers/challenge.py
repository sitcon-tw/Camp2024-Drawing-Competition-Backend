from django.urls import path

from api.views.challenge import (
    ChallengeAPIView,
    ChallengeRetrieveAPIView,
    ChallengeRetrieveSingleAPIView,
    ChallengeTeamListAPIView,
)

urlpatterns = [
    # Challenge Routes
    path("", ChallengeAPIView.as_view(), name="challenge"),
    path(
        "<int:pk>/",
        ChallengeRetrieveAPIView.as_view(),
        name="challenge-operate",
    ),
    path(
        "<int:pk>/test/",
        ChallengeRetrieveSingleAPIView.as_view(),
        name="challenge-single-operate",
    ),
    path("team/", ChallengeTeamListAPIView.as_view(), name="challenge-team"),
]

from django.urls import path
from api.views.submission import (
    SubmissionAPIView,
    SubmissionChallengeTeamAPIView,
    SubmissionChallengeTeamMaxAPIView,
    SubmissionTeamAPIView,
)

urlpatterns = [
    # Submission Routes
    path("", SubmissionAPIView.as_view(), name="submission"),
    path(
        "<int:team_id>/",
        SubmissionTeamAPIView.as_view(),
        name="submission-team",
    ),
    path(
        "challenge/<int:challenge_id>/team/<int:team_id>/",
        SubmissionChallengeTeamAPIView.as_view(),
        name="submission-challenge-team",
    ),
    path(
        "max/challenge/<int:challenge_id>/team/<int:team_id>/",
        SubmissionChallengeTeamMaxAPIView.as_view(),
        name="max-submission-challenge-team",
    ),
]

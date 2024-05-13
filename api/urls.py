from django.urls import path
from api.views.round import RoundAPIView, RoundListCreateAPIView
from api.views.user import (
    Register,
    LogoutAPI,
    EditProfileAPI,
    UserAPIView,
    LoginView,
)
from api.views.team import TeamAPIView, TeamTokenAPIView
from api.views.submission import SubmissionAPIView, SubmissionTeamAPIView
from api.views.challenge import (
    ChallengeAPIView,
    ChallengeRUDAPIView,
    ChallengeTeamAPIView,
)
from api.views.statistic import TeamChallengeScoreStaticAPIView

urlpatterns = [
    # Account Routes
    path("account/register/", Register.as_view(), name="account-register"),
    path("account/login/", LoginView.as_view(), name="account-login"),
    path("account/logout/", LogoutAPI.as_view(), name="account-logout"),
    path(
        "account/profile/edit/", EditProfileAPI.as_view(), name="account-profile-edit"
    ),
    path("account/user/all/", UserAPIView.as_view(), name="account-list"),
    # Teams Routes
    path("team/", TeamAPIView.as_view(), name="team"),
    path("team/<str:token>/", TeamTokenAPIView.as_view(), name="team-token"),
    # Submission Routes
    path("submission/", SubmissionAPIView.as_view(), name="submission"),
    path(
        "submission/<int:team_id>/",
        SubmissionTeamAPIView.as_view(),
        name="submission-team",
    ),
    # Challenge Routes
    path("challenge/", ChallengeAPIView.as_view(), name="challenge"),
    path(
        "challenge/<int:challenge_id>/",
        ChallengeRUDAPIView.as_view(),
        name="challenge-operate",
    ),
    path(
        "challenge/<int:challenge_id>/team/<int:team_id>/",
        ChallengeTeamAPIView.as_view(),
        name="challenge-submission-team",
    ),
    # Round Routes
    path("round/", RoundListCreateAPIView.as_view(), name="round"),
    path("round/<int:pk>/", RoundAPIView.as_view(), name="round-detail"),
    # Statistic Routes
    path(
        "statistic/team/",
        TeamChallengeScoreStaticAPIView.as_view(),
        name="statistic-team",
    ),
]

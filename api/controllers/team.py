from django.urls import path
from api.views.team import TeamAPIView, TeamAuthAPIView, TeamTokenAPIView


urlpatterns = [
    # Teams Routes
    path("", TeamAPIView.as_view(), name="team"),
    path("<str:token>/", TeamTokenAPIView.as_view(), name="team-token"),
    path("auth/token/", TeamAuthAPIView.as_view(), name="team-auth"),
]

from django.urls import include, path

urlpatterns = [
    # Account Routes
    path("account/", include("api.controllers.account")),
    # Teams Routes
    path("team/", include("api.controllers.team")),
    # Submission Routes
    path("submission/", include("api.controllers.submission")),
    # Challenge Routes
    path("challenge/", include("api.controllers.challenge")),
    # Round Routes
    path("round/", include("api.controllers.round")),
    # Statistic Routes
    path("statistic/", include("api.controllers.statistic")),
]

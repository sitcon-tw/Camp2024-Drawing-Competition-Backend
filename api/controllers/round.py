from django.urls import path
from api.views.round import RoundAPIView, RoundListCreateAPIView

urlpatterns = [
    # Round Routes
    path("", RoundListCreateAPIView.as_view(), name="round"),
    path("<int:pk>/", RoundAPIView.as_view(), name="round-detail"),
]

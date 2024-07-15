from django.urls import path
from api.views.clip import ClipAPIView

urlpatterns = [
    # Round Clips
    # Calculate the similarity between two images
    path("", ClipAPIView.as_view(), name="clip"),
]

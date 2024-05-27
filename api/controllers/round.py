from django.urls import path
from api.views.round import RoundAPIView, RoundListAPIView

urlpatterns = [
    # Round Routes
    # 列出符合當前時間的回合
    path("", RoundListAPIView.as_view(), name="round"),
    # 取得特定 ID 的回合資訊
    path("<int:pk>/", RoundAPIView.as_view(), name="round-detail"),
]

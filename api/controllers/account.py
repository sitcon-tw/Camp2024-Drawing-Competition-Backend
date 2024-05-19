from django.urls import path
from api.views.user import (
    Register,
    LogoutAPI,
    EditProfileAPI,
    UserAPIView,
    LoginView,
)

urlpatterns = [
    # Account Routes
    path("register/", Register.as_view(), name="account-register"),
    path("login/", LoginView.as_view(), name="account-login"),
    path("logout/", LogoutAPI.as_view(), name="account-logout"),
    path("profile/edit/", EditProfileAPI.as_view(), name="account-profile-edit"),
    path("", UserAPIView.as_view(), name="account-list"),
]

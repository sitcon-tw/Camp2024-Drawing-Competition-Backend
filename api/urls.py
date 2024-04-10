from django.urls import path
from api.views.user import (
    Register,
    LogoutAPI,
    EditProfileAPI,
    UserAPIView,
    OAuthUserRegisterAPI,
    OAuthUserLoginAPI,
    LoginView,
)
from api.views.order import OrderViewSet, OrderOperateViewSet, OrderScheduleViewSet
from api.views.part import PartListCreateViewSet, PartRetrieveUpdateDestroyViewSet


urlpatterns = [
    # Account Routes
    path("account/register/", Register.as_view(), name="account-register"),
    path("account/login/", LoginView.as_view(), name="account-login"),
    path("account/logout/", LogoutAPI.as_view(), name="account-logout"),
    path(
        "account/profile/edit/", EditProfileAPI.as_view(), name="account-profile-edit"
    ),
    path("account/user/all/", UserAPIView.as_view(), name="account-list"),
    # OAuth Routes
    path(
        "account/oauth/register/",
        OAuthUserRegisterAPI.as_view(),
        name="account-oauth-register",
    ),
    path(
        "account/oauth/login/", OAuthUserLoginAPI.as_view(), name="account-oauth-login"
    ),
    # Order Routes
    path(
        "order/",
        OrderViewSet.as_view(
            {
                "get": "find_all",
                "post": "add",
            }
        ),
        name="order-create-list",
    ),
    path("order/schedule/", OrderScheduleViewSet.as_view(), name="order-schedule"),
    path("order/<int:pk>/", OrderOperateViewSet.as_view(), name="order-get-put-delete"),
    # Part Routes
    path("part/", PartListCreateViewSet.as_view(), name="part-create-list"),
    path(
        "part/<int:pk>/",
        PartRetrieveUpdateDestroyViewSet.as_view(),
        name="part-get-put-delete",
    ),
]

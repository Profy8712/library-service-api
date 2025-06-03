from django.urls import path
from users.views import (
    UserRegisterView,
    UserProfileView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserProfileView.as_view(), name="profile"),
]

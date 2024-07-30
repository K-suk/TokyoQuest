# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CustomAuthToken, UserViewSet, LogoutView, PasswordChange, PasswordChangeDone, PasswordReset, PasswordResetDone, PasswordResetConfirm, PasswordResetComplete, ProfileView, ProfileEditView, user_reports

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')

# app_name = "accounts"

# urlpatterns = [
#     path('', include(router.urls)),
#     path('login/', CustomAuthToken.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('password_change/', PasswordChange.as_view(), name='password_change'),
#     path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
#     path('password_reset/', PasswordReset.as_view(), name='password_reset'),
#     path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
#     path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),
#     path('profile/', ProfileView.as_view(), name='profile'),
#     path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
#     path('reports/', user_reports, name='reports'),
# ]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import logout, profile, update_profile, change_password, password_reset_request, password_reset

app_name = "accounts"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('password-reset-request/', password_reset_request, name='password_reset_request'),
    path('password-reset/', password_reset, name='password_reset'),
]
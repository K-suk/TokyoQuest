from django.urls import path
from accounts.views import GoogleLogin

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
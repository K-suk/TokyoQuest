from django.contrib.auth.forms import AuthenticationForm # 追加

from .models import User

class LoginFrom(AuthenticationForm):
    class Meta:
        model = User
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(account_id=settings.SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                first_name = settings.SUPERUSER_FIRST_NAME,
                first_name = settings.SUPERUSER_LAST_NAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            print("スーパーユーザー作成")
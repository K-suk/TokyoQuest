from axes.signals import user_locked_out
from django.dispatch import receiver
from rest_framework.exceptions import PermissionDenied


@receiver(user_locked_out)
def user_locked(*args, **kwargs):
    raise PermissionDenied("ご利用のアカウントは凍結されています。しばらく経ってからログインしてください")

def get_account_id(request, credentials):
    account_id = credentials.get('account_id')
    if account_id:
        return account_id
    # Additional logic if needed, for example, if the user is not found or account_id is not provided
    return None
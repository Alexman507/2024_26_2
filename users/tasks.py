from datetime import timezone

from celery import shared_task
from dateutil.relativedelta import relativedelta

from users.models import User


@shared_task
def block_users_who_was_absent_last_mount():
    users_login = User.objects.filter(last_login__isnull=False, is_active=True,
                                      last_login=timezone.now() - relativedelta(months=1))
    users_login.update(is_active=False)

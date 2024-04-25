from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from src.key.models import AccessKey
from .utils import sendEmail

@shared_task
def expire_access_keys():
    # Get all active access keys whose expiry date has passed
    expired_keys = AccessKey.objects.filter(status="active", expiry_date__lte=timezone.now())

    # Set the status of expired keys to "expired"
    for key in expired_keys:
        key.status = "expired"
        key.save()
        key_user = key.owner
        
        # Send email to the key owner
        data = {
            "owner": key_user.full_name,
            "expiry_date": key.expiry_date,
        }
        sendEmail(keyExpired=True, recipient=key_user.email, keyData=data)
    return "Done!"
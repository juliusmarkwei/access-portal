from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from src.key.models import AccessKey
from .utils import sendEmail
import logging

logger = logging.getLogger(__name__)


@shared_task
def expire_access_keys():
    try:
        # Get all active access keys whose expiry date has passed
        expired_keys = AccessKey.objects.filter(
            status="active", expiry_date__lte=timezone.now()
        )

        # Set the status of expired keys to "expired"
        for key in expired_keys:
            key.status = "expired"
            key.save()
            key_owner = key.owner

            # Send email to the key owner
            data = {
                "owner": key_owner.full_name,
                "expiry_date": key.expiry_date.strftime("%d %B, %Y %H:%M %p"),
                "key_tag": key.key_tag,
            }
            sendEmail(keyExpired=True, recipient=key_owner.email, keyData=data)
        logger.info(f"Number of keys expired: {len(expired_keys)}")
        return "Done!"
    except Exception as e:
        logger.error(f"Error in expire_access_keys task: {e}")
        return f"Error: {e}"

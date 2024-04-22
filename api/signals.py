from django.dispatch import receiver
from django.db.models.signals import post_save
from key.models import AccessKey
from .utils import sendEmail


@receiver(post_save, sender=AccessKey)
def send_expired_access_key_mailing(sender, instance, created, **kwargs):
    if instance.expiry_date == "expired":
        data = {
            "owner": instance.owner,
            "expiry_date": instance.expiry_date,
        }
        sendEmail(keyExpired=True, recipient=instance.owner.email, keyData=data)

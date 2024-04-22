import string
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def generateAccessKey() -> str:
    """
    Generate a random access key
    """

    alphabet = string.ascii_letters + string.digits
    key = "".join(secrets.choice(alphabet) for i in range(80))
    return key


def sendEmail(
    accessGranted=False,
    KeyRevoked=False,
    keyExpired=False,
    recipient=None,
    keyData=None,
) -> None:
    """_summary_

    Args:
        accessGranted (bool, optional): if True, send accessGranted Message to user. Defaults to False.
        keyRevoked (bool, optional): if True, send keyRevoked Message to user. Defaults to False.
        keyExpired (bool, optional): if True, send keyExpred Message to user. Defaults to False.
        keyData (dict, optional): Access Key Data. Defaults to None.
    """
    if accessGranted:
        title = "Access Key Activated ✅"
        message = f"Dear {keyData.get('owner')}, \n\nWe are pleased to inform you that your access key has been successfully activated and it's scheduled to expire at {keyData.get('expiry_date')} (30 days). You can now enjoy full access to our system and its features."

    elif KeyRevoked:
        title = "Access Key Revoked ❌"
        message = f"Dear {keyData['owner']}, \n\nWe regret to inform you that your access key has been revoked. This could be due to a violation of our terms of service. Please contact us if you believe this is an error."

    elif keyExpired:
        title = "Access Key Expired :negative_squared_cross_mark:"
        message = f"Dear {keyData['owner']}, \n\nWe regret to inform you that your access key has expired. You can generate a new key by logging into your AccessPortal account."

    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False,
    )

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
    key = "".join(secrets.choice(alphabet) for i in range(50))
    return "AP-" + key


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
        title = "Access Key Activated"
        message = f"Hi {keyData['owner']}, \n\nWe are pleased to inform you that your access key ({keyData['key_tag']}) has been successfully activated and it's scheduled to expire on the {keyData['expiry_date']} - {keyData['validity_days']} day(s). You can now enjoy full access to our system and its features.\
            \n\nThank you for choosing Access Portal."

    elif KeyRevoked:
        title = "Access Key Revoked"
        message = f"Hi {keyData['owner']}, \n\nWe regret to inform you that your access key ({keyData['key_tag']}) has been revoked. This could be due to a violation of our terms of service. Please contact us if you believe this is an error.\
            \n\nThank you for your understanding."

    elif keyExpired:
        title = "Access Key Expired"
        message = f"Hi {keyData['owner']}, \n\nWe regret to inform you that your access key ({keyData['key_tag']})  has expired as of {keyData['expiry_date']}. This means that you will no longer be able to access our system using the provided access key.\
            \nIf you require continued access to our system, please log into ypur account to request a new access key.\
            \n\nThank you for choosing Access Portal."

    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False,
    )


# Notification email to admins
def reminderEmail(keyData: dict, admins: list) -> None:
    title = "Access Key Request"
    message = f"Hi Admin, \n\nA new access key request has been made by {keyData['owner']} - ({keyData['email']}). Kindly review the request and take the necessary action.\
        \n\nThank you."
    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        admins,
        fail_silently=False,
    )

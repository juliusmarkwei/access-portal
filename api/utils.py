import string
import secrets


def generateAccessKey() -> str:
    """
    Generate a random access key
    """

    alphabet = string.ascii_letters + string.digits
    key = "".join(secrets.choice(alphabet) for i in range(80))
    return key

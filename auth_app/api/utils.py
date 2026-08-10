from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings


def generate_user_token(user):
    """Generates a unique token for the user, which can be used for account
    activation or password reset.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_activation_email(user, domain="localhost:8000"):
    """Sends an account activation email to the user with a unique activation link."""
    uid, token = generate_user_token(user)

    activation_link = (
        f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"
    )

    send_mail(
        "Activate account.",
        f"Please activate your account: {activation_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return token


def send_password_reset_email(user, domain="localhost:8000"):
    """Sends a password reset email to the user with a unique reset link."""
    uid, token = generate_user_token(user)
    reset_link = f"{settings.FRONTEND_URL}/pages/auth/password_confirm.html?uid={uid}&token={token}"
    send_mail(
        "Reset password",
        f"Use this link to reset your password: {reset_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def decode_uid(uidb64):
    """Decodes the base64 encoded user ID from the URL and returns the original user ID."""
    try:
        return force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return None

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings


def generate_user_token(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uid, token


def send_activation_email(user, domain="localhost:8000"):
    uid, token = generate_user_token(user)
    activation_link = f"http://{domain}/api/activate/{uid}/{token}/"
    send_mail(
        "Activate account.",
        f"Please activate your account: {activation_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    return token


def send_password_reset_email(user, domain="localhost:8000"):
    uid, token = generate_user_token(user)
    reset_link = f"http://{domain}/api/password_confirm/{uid}/{token}/"
    send_mail(
        "Reset password",
        f"Use this link to reset your password: {reset_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def decode_uid(uidb64):
    try:
        return force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return None

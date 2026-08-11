from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os


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
    frontend_url = getattr(settings, "FRONTEND_URL", "http://127.0.0.1:5500")
    activation_link = f"{frontend_url}/pages/auth/activate.html?uid={uid}&token={token}"
    subject = "Confirm your email"
    context = {
        "username": user.username or user.first_name or "User",
        "activation_link": activation_link,
    }

    html_content = render_to_string("emails/account_activation_email.html", context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Activation link: {activation_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")

    logo_path = os.path.join(
        settings.BASE_DIR, "content", "static", "content", "images", "logo.png"
    )

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_mime = MIMEImage(f.read(), _subtype="png")
            logo_mime.add_header("Content-ID", "<videoflix_logo>")
            logo_mime.add_header("Content-Disposition", "inline", filename="logo.png")
            msg.attach(logo_mime)
    else:
        print(f" Logo not found: {logo_path}")

    msg.send()

    return token


# def send_password_reset_email(user, uid, token):
def send_password_reset_email(user, domain="localhost:8000"):
    """Sends a password reset email to the user with a unique reset link."""
    uid, token = generate_user_token(user)
    frontend_url = getattr(settings, "FRONTEND_URL", "http://127.0.0.1:5500")
    reset_link = (
        f"{frontend_url}/pages/auth/confirm_password.html?uid={uid}&token={token}"
    )

    subject = "Reset your Password"
    context = {
        "user": user,
        "reset_link": reset_link,
    }

    html_content = render_to_string("emails/password_reset_email.html", context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Reset link: {reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")

    logo_path = os.path.join(
        settings.BASE_DIR, "content", "static", "content", "images", "logo.png"
    )

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_mime = MIMEImage(f.read(), _subtype="png")
            logo_mime.add_header("Content-ID", "<videoflix_logo>")
            logo_mime.add_header("Content-Disposition", "inline", filename="logo.png")
            msg.attach(logo_mime)
    else:
        print(f" Logo not found: {logo_path}")

    msg.send()


def decode_uid(uidb64):
    """Decodes the base64 encoded user ID from the URL and returns the original user ID."""
    try:
        return force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return None

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordConfirmSerializer,
)
from .utils import send_activation_email, send_password_reset_email, decode_uid

User = get_user_model()


class RegisterView(APIView):
    """Handles user registration and sends an activation email."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                token = send_activation_email(user)
            except Exception as e:
                print(f"Email sending failed: {e}")
                token = None

            return Response(
                {"user": {"id": user.id, "email": user.email}, "token": token},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "Please check your entries and try again."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ActivateView(APIView):
    """Handles account activation via a unique token sent to the user's email."""

    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        uid = decode_uid(uidb64)
        user = User.objects.filter(pk=uid).first() if uid else None
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"message": "Account successfully activated."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Activation failed."}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """Handles user login and returns per Cookies JWT tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Please check your entries."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user or not user.is_active:
            return Response(
                {"detail": "Invalid login credentials or user is inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {
                "detail": "Login successful",
                "user": {"id": user.id, "username": user.email},
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=False,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Lax",
            secure=False,
        )

        return response


class LogoutView(APIView):
    """Handles user logout by blacklisting the refresh token and deleting cookies."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        response = Response(
            {
                "detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."
            },
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(APIView):
    """Handles refreshing the access token using the refresh token stored in cookies."""

    permission_classes = [permissions.AllowAny]
    """Ignore expired access tokens."""
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            response = Response(
                {"detail": "Token refreshed", "access": new_access},
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                "access_token", new_access, httponly=True, samesite="Lax"
            )
            return response
        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class PasswordResetView(APIView):
    """Handles password reset requests by sending a reset email to the user."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                send_password_reset_email(user)
        return Response(
            {"detail": "An email has been sent to reset your password."},
            status=status.HTTP_200_OK,
        )


class PasswordConfirmView(APIView):
    """Handles password reset confirmation by validating the token and setting
    the new password."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uid = decode_uid(uidb64)
        user = User.objects.filter(pk=uid).first() if uid else None
        if user and default_token_generator.check_token(user, token):
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Your Password has been successfully reset."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST
        )

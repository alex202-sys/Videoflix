from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Validates that the password and confirmed_password match.
    """

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirmed_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """
        Validate that the password and confirmed_password match.
        """
        if attrs["password"] != attrs.pop("confirmed_password"):
            raise serializers.ValidationError(
                "Please check your entries and try again. Passwords do not match."
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        The user is created with is_active set to False.
        """
        email = validated_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            is_active=False,
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request."""

    email = serializers.EmailField()


class PasswordConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a new password."""

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

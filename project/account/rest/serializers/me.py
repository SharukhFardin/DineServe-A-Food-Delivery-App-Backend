import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from shared.choices import StatusChoices

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Get email and password from input data
        email = data.get("email", None)
        password = data.get("password", None)

        # Check if email and password is provided
        if email is None or password is None:
            raise serializers.ValidationError("Both email and password are required.")

        # Authenticate user
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        # Check if the account is active or not
        if not user.is_active:
            raise serializers.ValidationError("User account is deactivated.")

        # Insert user object in data dictionary
        data["user"] = user
        return data


class PublicUserRegistrationSerializer(serializers.Serializer):
    """Serializer for User registration."""

    first_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    phone = PhoneNumberField(allow_blank=True, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=5,
        max_length=100,
        write_only=True,
    )
    address = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(allow_empty_file=True, required=False)

    def validate_email(self, value):
        """Validate that the email doesn't already exist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        """Validate that the email doesn't already exist."""
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        # Performing checks for strong password: 1 uppercase, 1 lowercase, 1 number, 1 special character
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value

    def validate(self, data):
        "Checks if passwords match; skips if confirm_password is missing."

        password = data.get("password")
        confirm_password = data.get("confirm_password", None)

        if confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        # Removing confirm_password field from validated data
        validated_data.pop("confirm_password", None)

        # Create a new user with the provided data
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone", None),
            address=validated_data.get("address", ""),
            image=validated_data.get("image", None),
            password=make_password(
                validated_data.get("password")
            ),  # Hashing the password
            status=StatusChoices.ACTIVE,
        )

        return user

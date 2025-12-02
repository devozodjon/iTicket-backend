from django.contrib.auth import authenticate
from rest_framework import serializers, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models.user import User, VerificationCode
from apps.users.utils.code_generators import (
    generate_unique_username,
    generate_verification_code,
    send_email
)


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("This email already registered")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=generate_unique_username(),
            password=password,
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            is_active=False
        )

        code = generate_verification_code()
        VerificationCode.objects.create(user=user, code=code)

        send_email(receiver_email=user.email, body=f"Your code: {code}")

        return user


class VerifyCodeSerializer(serializers.Serializer):
    """Check verification code and activate user"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        try:
            verification = VerificationCode.objects.filter(user=user, code=code, used=False).latest("created_at")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired code")

        if not verification.is_valid():
            raise serializers.ValidationError("Verification code is expired")

        verification.used = True
        verification.save()
        user.is_active = True
        user.is_email_verified = True
        user.save()

        attrs["user"] = user
        return attrs



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email or password is incorrect.")

        if not user.is_active:
            raise serializers.ValidationError("Email not verified.")

        attrs["user"] = user
        return attrs


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
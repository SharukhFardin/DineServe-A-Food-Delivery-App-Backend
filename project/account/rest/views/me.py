from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..serializers.me import UserLoginSerializer, PublicUserRegistrationSerializer


class UserLoginView(APIView):
    """Apiview for user login and returning token with success message"""

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            # Get user object from validated data
            user = serializer.validated_data["user"]

            # Get or create token for the user. Although by signal the token was certainly created.
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "message": "Successefully Logged In!",
                    "name": f"{user.first_name} {user.last_name}",
                    "email": user.email,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserRegistrationView(CreateAPIView):
    """View for User registration."""

    serializer_class = PublicUserRegistrationSerializer
    permission_classes = [AllowAny]

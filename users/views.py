from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.validated_data)
        return Response(data={'user.id': user.id}, status=status.HTTP_201_CREATED)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)
        return Response(data={'error': 'User not valid!'}, status=status.HTTP_401_UNAUTHORIZED)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not code:
            confirm_code, created = ConfirmCode.objects.get_or_create(user=user)
            confirm_code.generate_code()
            return Response({'message': 'Confirmation code generated.', 'code': confirm_code.code},
                            status=status.HTTP_200_OK)

        try:
            confirm_code = user.confirm_code
            if confirm_code.code != code:
                return Response({'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()

            confirm_code.delete()

            return Response({'message': 'User confirmed successfully.'}, status=status.HTTP_200_OK)

        except ConfirmCode.DoesNotExist:
            return Response({'error': 'No confirmation code found for this user.'}, status=status.HTTP_400_BAD_REQUEST)

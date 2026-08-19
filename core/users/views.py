from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import redirect
from rest_framework.throttling import AnonRateThrottle
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here


class LoginRateThrottle(AnonRateThrottle):
    rate = '5/min'


User = get_user_model()

def issue_jwt_and_redirect(backend, user, response, *args, **kwargs):
    if not user:
        return
    if not user.is_active:
        user.is_active = True
        user.save()    
    
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    frontend_url = os.environ.get('FRONTEND_URL', '127.0.0.1:3000')

    response = redirect(f'https://{frontend_url}/dashboard?access={access_token}')
    
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='None',
        max_age=7 * 24 * 60 * 60
    )

    return response

class CustomLoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {'access': access_token},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
            max_age=7 * 24 * 60 * 60
        )

        return response


class CustomRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'No refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response(
                {'access': access_token},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CustomLogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'No refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except TokenError:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('refresh_token')
        return response
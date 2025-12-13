from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterUserSerializer, LoginUserSerializer

@api_view(['GET'])
def health_check(request):
    return Response({"status":"running"})


@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)

    # If validation fails, raises an exception automatically (400 - Bad Request)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(
        {
            "id": user.id,
            "username": user.username
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def login_user(request):
    serializer = LoginUserSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
    except serializers.ValidationError:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = serializer.validated_data["user"]

    return Response(
        {
            "id": user.id,
            "username": user.username
        },
        status=status.HTTP_200_OK
    )

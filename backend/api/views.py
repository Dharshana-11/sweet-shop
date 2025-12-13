from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterUserSerializer

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
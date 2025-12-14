from unicodedata import category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Sweet
from .serializers import SweetSerializer


@api_view(['GET', 'POST'])

# Only logged-in users can access this API
@permission_classes([IsAuthenticated])
def sweets_list(request):

    # If request is GET, return all sweets from the DB
    if request.method == 'GET':
        queryset = Sweet.objects.all()  # fetch all sweet records
        serializer = SweetSerializer(queryset, many=True)  # convert data to JSON
        return Response(serializer.data)  # send data as response

    # If the request is POST, create new sweet
    serializer = SweetSerializer(data=request.data)  # take input data from request
    serializer.is_valid(raise_exception=True)  
    serializer.save()  

    # Return created sweet data with success status
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sweets_search(request):

    queryset = Sweet.objects.all()  # fetch all sweet records

    name = request.query_params.get("name")
    category = request.query_params.get("category")
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")

    if name:
        queryset = queryset.filter(name_icontains = name)

    if category:
        queryset = queryset.filter(category__iexact = category) # Filters and stores only matching categories data (case-insensitive)

    if min_price:
        queryset = queryset.filter(price__gte = min_price) # Filters sweets that have price greater than or equal to min_price

    if max_price:
        queryset = queryset.filter(price__lte = max_price) # Filters greater than or equal to min_price

    serializer = SweetSerializer(queryset, many=True)  # convert data to JSON
    return Response(serializer.data)  # send data as response

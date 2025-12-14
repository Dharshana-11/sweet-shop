from unicodedata import category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Sweet
from .serializers import SweetSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from django.db.models import F


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
        # Filters and stores only matching categories data (case-insensitive)
        queryset = queryset.filter(category__iexact = category) 

    if min_price:
        # Filters sweets that have price greater than or equal to min_price
        queryset = queryset.filter(price__gte = min_price) 

    if max_price:
        # Filters greater than or equal to min_price
        queryset = queryset.filter(price__lte = max_price) 

    serializer = SweetSerializer(queryset, many=True)  # convert data to JSON
    return Response(serializer.data)  


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sweet(request, id):

    #If sweet doesn’t exist then 404 Not Found
    sweet = get_object_or_404(Sweet, id=id)

    # Pass existing object (sweet) and new data
    serializer = SweetSerializer(
        sweet,
        data=request.data
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser]) #IsAdminUser automatically checks user.is_staff is True
def delete_sweet(request, id):
    sweet = get_object_or_404(Sweet, id=id)
    sweet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Helper Function for inventory
def sweet_inventory_response(sweet):
    return {
        "id": sweet.id,
        "name": sweet.name,
        "quantity": sweet.quantity,
    }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_sweet(request, id):

    # Transaction makes sure multiple database operations happen safely (Either all queries succeed or none of them are saved)
    with transaction.atomic():
        sweet = get_object_or_404(Sweet, id=id)

        if sweet.quantity <= 0:
            return Response(
                {"detail": "Sweet is out of stock"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # F expression is used to update afield based on its current value in the DB without bringing values into Python
        Sweet.objects.filter(id=id).update(quantity=F('quantity') - 1)
        sweet.refresh_from_db()

    return Response(
        sweet_inventory_response(sweet),
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def restock_sweet(request, id):
    amount = request.data.get("amount")

    # If amt is empty, not a valid integer or lesser than zero, 400 is raised
    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return Response(
            {"detail": "Valid restock amount is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    sweet = get_object_or_404(Sweet, id=id)

    Sweet.objects.filter(id=id).update(quantity=F('quantity') + amount)
    sweet.refresh_from_db()

    return Response(
        sweet_inventory_response(sweet),
        status=status.HTTP_200_OK
    )

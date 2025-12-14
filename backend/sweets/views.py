from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Sweets
from .serailizers import SweetsSerializer
from rest_framework import status

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def sweets_list(request):
    if request.method == "GET":
        sweets = Sweets.objects.all()
        serializer = SweetsSerializer(sweets, many=True)
        return Response(serializer.data)
    
    serializer = SweetsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
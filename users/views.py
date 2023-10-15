from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tier
from .serializers import TierSerializer, ThumbnailSizeSerializer


class CustomTierCreateView(APIView):
    serializer_class = TierSerializer

    def get(self, request):
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TierSerializer(data=request.data)
        if serializer.is_valid():
            tier = serializer.save()
            return Response({'message': 'Custom Tier created successfully', 'tier_id': tier.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import mimetypes
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from django.http import FileResponse
from rest_framework.response import Response

from .models import Image, ExpiringLink
from .mixins import ExpiringLinkMixin
from .permissions import IsAdminOrAllowed
from .serializers import (ImageListSerializer,
                          ImageCreateSerializer,
                          ExpiringLinkCreateSerializer,
                          ExpiringLinkListSerializer)


class ImageListAPIView(generics.ListAPIView):
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ImageCreateAPIView(generics.CreateAPIView):
    serializer_class = ImageCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExpiringLinkListCreateAPIView(generics.ListCreateAPIView, ExpiringLinkMixin):
    permission_classes = [IsAdminOrAllowed]

    def get_queryset(self):
        return ExpiringLink.objects.filter(image__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpiringLinkCreateSerializer
        return ExpiringLinkListSerializer

    def create(self, request, *args, **kwargs):
        image_id = request.data.get('image')
        try:
            image = Image.objects.get(id=image_id, user=request.user)
        except Image.DoesNotExist:
            return Response({'detail': 'You can only create expiring links for your own images.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        response = super().create(request, *args, **kwargs)
        response.data = self.link
        return response

    def perform_create(self, serializer):
        expiring_time = self.request.data.get('expiring_time')
        self.link = self.generate_expiring_link(serializer.validated_data['image'], expiring_time)


class ExpiringLinkDetailAPIView(generics.RetrieveAPIView, ExpiringLinkMixin):
    queryset = ExpiringLink.objects.all()
    permission_classes = [IsAdminOrAllowed]

    def get_object(self):
        signed_link = self.kwargs.get('signed_link')

        expiring_link_id = self.decode_signed_link(signed_link)
        expiring_link = generics.get_object_or_404(self.queryset, pk=expiring_link_id)
        if expiring_link.is_expired():
            expiring_link.delete()
            raise NotFound("Link has expired")

        # if expiring_link.image.user != self.request.user:
        #     raise PermissionDenied("User is not authorized to view expiring link")

        return expiring_link.image

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image
        content_type, _ = mimetypes.guess_type(image.name)
        response = FileResponse(image, content_type=content_type, as_attachment=False,
                                filename=image.name.split('/')[-1])
        return response

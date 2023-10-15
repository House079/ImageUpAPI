from rest_framework import serializers
from .models import Image, ExpiringLink
from .validators import validate_image_extension


class ImageListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['images']

    def get_images(self, obj):
        request = self.context.get('request')
        return obj.get_links(request)


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_image_extension])

    class Meta:
        model = Image
        fields = ['title', 'image']


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['link']


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpiringLink
        fields = ['image', 'expiring_time']


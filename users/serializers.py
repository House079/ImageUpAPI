from rest_framework import serializers
from .models import Tier, ThumbnailSize


class ThumbnailSizeSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()

    class Meta:
        model = ThumbnailSize
        fields = ['width', 'height']

    def to_internal_value(self, data):
        return ThumbnailSize(**data)

    def to_representation(self, instance):
        return {
            'width': instance.width,
            'height': instance.height
        }


class TierSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Tier
        fields = '__all__'

    def create(self, validated_data):
        thumbnail_sizes = validated_data.pop('thumbnail_size', [])

        tier = Tier.objects.create(**validated_data)

        thumbnail_size_objects = []
        for size in thumbnail_sizes:
            try:
                width, height = size.split('x')
                width = int(width)
                height = int(height)
                thumbnail_size = ThumbnailSize.objects.get_or_create(width=width, height=height)[0]
                thumbnail_size_objects.append(thumbnail_size)
            except (ValueError, IndexError):
                continue

        tier.thumbnail_size.set(thumbnail_size_objects)

        return tier
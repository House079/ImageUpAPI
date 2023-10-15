from rest_framework import serializers
import os


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']

    if ext.lower() not in valid_extensions:
        raise serializers.ValidationError("Only JPG and PNG files are allowed.")

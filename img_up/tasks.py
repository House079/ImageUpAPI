from __future__ import absolute_import, unicode_literals
import os
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.storage import default_storage
from .models import Image
from django.core.files.base import ContentFile
from rest_img.celery import app


@app.task
def convert_to_thumbnails(pk):
	instance = Image.objects.get(id=pk)
	print(instance)

	user_tier = instance.user.tier
	tier_thumbnails = user_tier.get_thumbnail_size
	filename, _ = os.path.splitext(os.path.basename(instance.image.name))
	image_name = filename.split("/")[-1]

	img_file = BytesIO(instance.image.read())
	image = PILImage.open(img_file)

	for size in tier_thumbnails:
		width, height = int(size.width), int(size.height)

		thumb = image.resize((width, height))

		thumbnail_io = BytesIO()
		thumb.save(
			thumbnail_io,
			format='JPEG',
			quality=100)
		thumbnail_name = f'{image_name}_thumbnail_{width}x{height}.jpg'

		thumbnail_content = ContentFile(thumbnail_io.getvalue())

		custom_path = f'{instance.user.id}/images/{pk}/{thumbnail_name}'

		thumbnail_path = default_storage.save(custom_path, thumbnail_content)

		thumbnail_io.close()

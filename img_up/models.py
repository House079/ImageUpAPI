import os
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
from .functions import path_to_upload_img
from users.models import Tier
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Image(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to=path_to_upload_img)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	@property
	def get_orignal_url(self):
		return self.image.url

	def get_links(self, request):
		user_tier = self.user.tier
		if user_tier is None:
			user_tier = Tier.objects.get(name='Basic')
		base_file = os.path.dirname(self.image.name)
		base_url = request.build_absolute_uri('/')
		thumbnails = default_storage.listdir(base_file)[1]
		links_for_user = []

		for thumbnail in thumbnails:
			if 'thumbnail' in thumbnail:
				thumbnails_path = os.path.join(base_file, thumbnail)
				links_for_user.append(base_url + settings.MEDIA_URL + thumbnails_path)

		if user_tier.supports_original_link:
			links_for_user.append(base_url + self.get_orignal_url)

		if user_tier.supports_expiring_link and hasattr(self, 'expiring_link'):
			links_for_user.append(self.expiring_link.link)

		return links_for_user


class ExpiringLink(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	image = models.OneToOneField(Image, on_delete=models.CASCADE, unique=True, related_name='expiring_link')
	link = models.CharField(max_length=255)
	expiring_time = models.IntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)])
	expired_at = models.DateTimeField()

	def __str__(self):
		return f'{self.link}'

	def is_expired(self):
		current_time = timezone.now()
		return current_time > self.expired_at


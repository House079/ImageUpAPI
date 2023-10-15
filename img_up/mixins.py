from datetime import datetime
import uuid
from django.core import signing
from django.urls import reverse
from .models import ExpiringLink
from rest_framework.exceptions import NotFound


class ExpiringLinkMixin:
	def generate_expiring_link(self, image, expiring_time):
		expiring_time = float(expiring_time)
		pk = uuid.uuid4()
		signed_link = signing.dumps(str(pk))

		url = self.request.build_absolute_uri(reverse('img_up:expiring_link_detail',
		                                              kwargs={'signed_link': signed_link}))

		current_timestamp = datetime.now().timestamp()
		expiration_timestamp = current_timestamp + expiring_time
		expired_at = datetime.fromtimestamp(expiration_timestamp)

		ExpiringLink.objects.create(id=pk, link=url, image=image, expiring_time=expiring_time, expired_at=expired_at)

		return {'link': url}

	@staticmethod
	def decode_signed_link(signed_link):
		try:
			return signing.loads(signed_link)
		except signing.BadSignature:
			raise NotFound('Invalid signed link')

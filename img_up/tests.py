import io
import os
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from .models import Image, ExpiringLink, User
from django.test import TestCase, override_settings
from users.models import CustomUser, Tier, ThumbnailSize
from img_up.models import Image
from img_up.signals import convert_to_thumbnails
from PIL import Image as PILImage
from rest_img import settings
from users.tests import create_default_tiers
import shutil


def generate_image_file(format, extension):
	file = io.BytesIO()
	image = PILImage.new('RGB', size=(800, 800), color=(255, 255, 255))
	image.save(file, format)
	file.name = f'test.{extension}'
	file.seek(0)
	return file


class EnterpriseUserUploadAPITest(TestCase):
	test_dir = os.path.join(settings.BASE_DIR, 'test_dir')

	def setUp(self):
		super().setUp()
		create_default_tiers(sender=None, connection=None)
		enterprise_tier = Tier.objects.get(name='Enterprise')
		self.user = get_user_model().objects.create_user(
			username='testuser',
			email='testuser@email.com',
			password='testpass123',
			tier=enterprise_tier
		)

		self.client.login(username='testuser', password='testpass123')
		self.jpg_file = generate_image_file('jpeg', 'jpg')
		self.jpg = Image.objects.create(image=self.jpg_file.name, user=self.user)

		self.png_file = generate_image_file('png', 'png')
		self.png = Image.objects.create(image=self.png_file.name, user=self.user)

		self.bmp_file = generate_image_file('bmp', 'bmp')
		self.bmp = Image.objects.create(image=self.bmp_file.name, user=self.user)

	@override_settings(MEDIA_ROOT=('test_dir' + '/media'))
	def test_upload_jpg_image(self):
		upload_url = reverse('img_up:upload_image')
		data = {'title': 'test title', 'image': self.jpg_file}
		response = self.client.post(upload_url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		image = Image.objects.latest('uploaded_at')
		convert_to_thumbnails(image.id)
		expected_subdirectory = f"{image.user.id}/images/{image.id}"

		expected_directory = os.path.join(self.test_dir, 'media', expected_subdirectory)

		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test.jpg')))
		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_200x200.jpg')))
		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_400x400.jpg')))

	@override_settings(MEDIA_ROOT=('test_dir' + '/media'))
	def test_upload_png_image(self):
		upload_url = reverse('img_up:upload_image')
		data = {'title': 'test title', 'image': self.png_file}
		response = self.client.post(upload_url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		image = Image.objects.latest('uploaded_at')
		convert_to_thumbnails(image.id)
		expected_subdirectory = f"{image.user.id}/images/{image.id}"

		expected_directory = os.path.join(self.test_dir, 'media', expected_subdirectory)

		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test.png')))
		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_200x200.jpg')))
		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_400x400.jpg')))

	@override_settings(MEDIA_ROOT=('test_dir' + '/media'))
	def test_upload_bmp_image(self):
		upload_url = reverse('img_up:upload_image')
		data = {'title': 'test title', 'image': self.bmp_file}
		response = self.client.post(upload_url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_image_list_api(self):
		url = reverse('img_up:image_list_api')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_expiring_link_creation(self):
		url = reverse('img_up:expiring_link')
		data = {'image': self.jpg.id, 'expiring_time': 300}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(ExpiringLink.objects.count(), 1)
		self.assertEqual(Image.objects.first().user, self.user)

	def test_expiring_link_list(self):
		url = reverse('img_up:expiring_link')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def tearDown(self):
		try:
			shutil.rmtree(self.test_dir)
		except OSError:
			pass


class BasicUserUploadAPITest(TestCase):
	test_dir = os.path.join(settings.BASE_DIR, 'test_dir')

	def setUp(self):
		super().setUp()
		create_default_tiers(sender=None, connection=None)
		basic_tier = Tier.objects.get(name='Basic')
		self.user = get_user_model().objects.create_user(
			username='testuser',
			email='testuser@email.com',
			password='testpass123',
			tier=basic_tier
		)

		self.client.login(username='testuser', password='testpass123')
		self.jpg_file = generate_image_file('jpeg', 'jpg')
		self.jpg = Image.objects.create(image=self.jpg_file.name, user=self.user)

	@override_settings(MEDIA_ROOT=('test_dir' + '/media'))
	def test_upload_jpg_image(self):
		upload_url = reverse('img_up:upload_image')
		data = {'title': 'test title', 'image': self.jpg_file}
		response = self.client.post(upload_url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		image = Image.objects.latest('uploaded_at')
		convert_to_thumbnails(image.id)
		expected_subdirectory = f"{image.user.id}/images/{image.id}"

		expected_directory = os.path.join(self.test_dir, 'media', expected_subdirectory)

		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test.jpg')))
		self.assertTrue(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_200x200.jpg')))
		self.assertFalse(os.path.exists(os.path.join(expected_directory, 'test_thumbnail_400x400.jpg')))

	def test_image_list_api(self):
		url = reverse('img_up:image_list_api')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_expiring_link_creation(self):
		url = reverse('img_up:expiring_link')
		data = {'image': self.jpg.id, 'expiring_time': 300}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_expiring_link_list(self):
		url = reverse('img_up:expiring_link')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def tearDown(self):
		try:
			shutil.rmtree(self.test_dir)
		except OSError:
			pass
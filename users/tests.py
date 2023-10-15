from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Tier, ThumbnailSize
from rest_framework import status


class CustomTierTestCase(TestCase):
	def setUp(self):
		self.admin_user = get_user_model().objects.create(username='admin', is_staff=True, is_superuser=True)
		self.admin_user.set_password('admin')
		self.admin_user.save()

		self.thumbnail_1 = ThumbnailSize.objects.create(width=200, height=200)
		self.thumbnail_2 = ThumbnailSize.objects.create(width=400, height=400)

	def test_create_custom_tier(self):
		self.client.login(username='admin', password='admin')

		response = self.client.post('/users/create-custom-tier/', {
			'name': 'Custom Tier 1',
			'thumbnail_size': [str(self.thumbnail_1), str(self.thumbnail_2)],
			'supports_expiring_link': True,
			'supports_original_link': True,
		})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Adjust the status code as needed
		custom_tier = Tier.objects.get(name='Custom Tier 1')
		self.assertEqual(custom_tier.thumbnail_size.count(), 2)

		self.assertIn(self.thumbnail_1, custom_tier.thumbnail_size.all())
		self.assertIn(self.thumbnail_2, custom_tier.thumbnail_size.all())
		self.assertTrue(custom_tier.supports_expiring_link)
		self.assertTrue(custom_tier.supports_original_link)


def create_default_tiers(**kwargs):
	# Create a list of tier definitions with their options
	tier_definitions = [
		{
			'name': 'Basic',
			'supports_original_link': False,
			'supports_expiring_link': False,
			'thumbnail_sizes': [(200, 200)],
		},
		{
			'name': 'Premium',
			'supports_original_link': True,
			'supports_expiring_link': False,
			'thumbnail_sizes': [(200, 200), (400, 400)],
		},
		{
			'name': 'Enterprise',
			'supports_original_link': True,
			'supports_expiring_link': True,
			'thumbnail_sizes': [(200, 200), (400, 400)],
		},
		{
			'name': 'Custom',
			'supports_original_link': False,
			'supports_expiring_link': True,
			'thumbnail_sizes': [(100, 100), (150, 150), (200, 200)],
		},

	]

	for tier_definition in tier_definitions:
		tier, _ = Tier.objects.get_or_create(name=tier_definition['name'])
		tier.supports_original_link = tier_definition['supports_original_link']
		tier.supports_expiring_link = tier_definition['supports_expiring_link']
		tier.save()

		for width, height in tier_definition['thumbnail_sizes']:
			thumbnail, _ = ThumbnailSize.objects.get_or_create(width=width, height=height)
			tier.thumbnail_size.add(thumbnail)


class CreateUserAndAssignTiersTestCase(TestCase):
	def setUp(self):
		create_default_tiers(sender=None, connection=None)

	def test_create_user_and_assign_tiers(self):
		user = get_user_model().objects.create(username='testuser', password='testpass', email='testemail')

		basic_tier = Tier.objects.get(name='Basic')
		premium_tier = Tier.objects.get(name='Premium')
		enterprise_tier = Tier.objects.get(name='Enterprise')
		custom_tier = Tier.objects.get(name='Custom')

		user.tier = basic_tier
		user.save()
		self.assertEqual(user.tier, basic_tier)

		user.tier = premium_tier
		user.save()
		self.assertEqual(user.tier, premium_tier)

		user.tier = enterprise_tier
		user.save()
		self.assertEqual(user.tier, enterprise_tier)

		user.tier = custom_tier
		user.save()
		self.assertEqual(user.tier, custom_tier)

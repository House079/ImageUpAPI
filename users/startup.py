from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tier, ThumbnailSize
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_default_tiers(**kwargs):
    basic_tier, _ = Tier.objects.get_or_create(
        name="Basic",
        supports_original_link=False,
        supports_expiring_link=False
    )
    basic_thumbnail, _ = ThumbnailSize.objects.get_or_create(width=200, height=200)
    basic_tier.thumbnail_size.add(basic_thumbnail)

    premium_tier, _ = Tier.objects.get_or_create(
        name="Premium",
        supports_original_link=True,
        supports_expiring_link=False
    )
    premium_thumbnail_1, _ = ThumbnailSize.objects.get_or_create(width=200, height=200)
    premium_thumbnail_2, _ = ThumbnailSize.objects.get_or_create(width=400, height=400)
    premium_tier.thumbnail_size.add(premium_thumbnail_1, premium_thumbnail_2)

    enterprise_tier, _ = Tier.objects.get_or_create(
        name="Enterprise",
        supports_original_link=True,
        supports_expiring_link=True
    )
    enterprise_tier.thumbnail_size.set([premium_thumbnail_1, premium_thumbnail_2])


@receiver(post_migrate)
def create_superuser(**kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print('Superuser created.')
    else:
        print('Superuser already exists.')

    enterprise_tier, created = Tier.objects.get_or_create(name='Enterprise')
    admin_user = User.objects.get(username='admin')
    admin_user.tier = enterprise_tier
    admin_user.save()
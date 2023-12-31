from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Image
from .tasks import convert_to_thumbnails


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance, created, **kwargs):
	if created:
		convert_to_thumbnails.delay(instance.id)

#
# @receiver(post_save, sender=Image)
# def create_thumbnails(sender, instance, created, **kwargs):
# 	if created:
# 		convert_to_thumbnails.apply_async(args=(instance.id,))

from django.contrib import admin
from .models import ExpiringLink, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'image', 'uploaded_at', 'user')


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
	list_display = ('image', 'link', 'expiring_time', 'expired_at')

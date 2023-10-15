import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f'{self.width}x{self.height}'


class Tier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    thumbnail_size = models.ManyToManyField(ThumbnailSize, blank=True)
    supports_expiring_link = models.BooleanField(default=False)
    supports_original_link = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    @property
    def get_thumbnail_size(self):
        return self.thumbnail_size.all()


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

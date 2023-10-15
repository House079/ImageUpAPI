from django.core.management.base import BaseCommand

from users.startup import create_default_tiers, create_superuser


class Command(BaseCommand):
    help = 'Create default tiers for the users app'

    def handle(self, *args, **options):
        create_default_tiers()
        create_superuser()





from django.core.management.base import BaseCommand
from datetime import datetime

from ...models import Etiquette, User


class Command(BaseCommand):
    help = 'Runs the monthly task'

    def handle(self, *args, **kwargs):
        print(Etiquette)
        print(f"Monthly task executed at {datetime.now()}")

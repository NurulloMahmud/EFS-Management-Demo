from django.core.management.base import BaseCommand
import random
from django.utils.crypto import get_random_string
from main.models import Efs
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the Efs model with random data'

    def handle(self, *args, **options):
        amounts = [50, 100, 200, 300, 400, 500, 600, 700, 800]

        for _ in range(90):
            code = get_random_string(length=10, allowed_chars='0123456789')
            reference = get_random_string(length=10, allowed_chars='0123456789')
            amount = random.choice(amounts)

            efs = Efs(code=code, reference=reference, amount=amount, date=timezone.now())
            efs.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated Efs model'))

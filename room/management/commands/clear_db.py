from django.core.management.base import BaseCommand
from room.models import Room, Player, Chess


class Command(BaseCommand):
    def handle(self, *args, **options):
        Chess.objects.all().delete()
        Room.objects.all().delete()
        Player.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared the db'))

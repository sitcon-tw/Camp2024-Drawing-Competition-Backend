import random
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import ProgrammingError
from django.utils.crypto import get_random_string
from django_seed import Seed
from api.models import Team


class Command(BaseCommand):
    help = "Create 10 teams for playing"
    seeder = Seed.seeder()

    def handle(self, *args, **options):
        for i in range(1, 11):  # 生成10個 Team
            team = Team(name=f"第{i}小隊", token=get_random_string(length=4))
            team.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created team {team.name}")
            )

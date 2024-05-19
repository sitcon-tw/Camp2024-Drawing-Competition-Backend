from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from api.models import Team


class Command(BaseCommand):
    help = "建立 10 個小隊並生成對應的 token"

    def handle(self, *args, **options):
        for i in range(1, 11):  # 生成10個 Team
            team = Team(name=f"第{i}小隊", token=get_random_string(length=4))
            team.save()
            self.stdout.write(self.style.SUCCESS(f"成功建立小隊-隊名:{team.name}"))

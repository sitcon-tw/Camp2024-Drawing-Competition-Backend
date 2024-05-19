from django.core.management.base import BaseCommand
from api.utils.toggle_rounds import toggle_rounds


class Command(BaseCommand):
    help = "Refresh Round Valid Status According Current Time"

    def handle(self, *args, **options):
        toggle_rounds()
        self.stdout.write(self.style.SUCCESS(f"成功更新回合狀態"))

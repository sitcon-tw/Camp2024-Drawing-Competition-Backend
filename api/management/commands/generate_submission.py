import datetime
import random
from django.core.management.base import BaseCommand
from api.models import Round, Challenge, Team, Submission


class Command(BaseCommand):
    help = "建立每小隊每回合每個挑戰各 3 份提交紀錄"

    def handle(self, *args, **options):
        for challenge in Challenge.objects.all():
            for team in Team.objects.all():
                submission = Submission.objects.create(
                    code=f"# {team.name} 的程式碼",
                    status=Submission.status_option[random.randint(0, 3)][0],
                    score=random.randint(0, 100),
                    fitness=random.randint(0, 100),
                    word_count=random.randint(0, 100),
                    execute_time=datetime.timedelta(seconds=random.randint(0, 10)),
                    stdout=f"# {team.name} 的標準輸出",
                    stderr=f"# {team.name} 的標準錯誤",
                    team=team,
                    challenge=challenge,
                    round_id=Round.objects.get(challenge.round_id),
                )
                submission.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"成功建立提交{submission.pk}-小隊{team.name}-回合{round.pk}-挑戰{challenge.pk}-分數{submission.score}"
                )
            )

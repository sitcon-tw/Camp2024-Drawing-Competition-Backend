import datetime
from django.core.management.base import BaseCommand
from api.models import Round


class Command(BaseCommand):
    help = (
        "建立 5 個回合，並根據活動時間自動往後推算開始/結束時間以及回合之間的間隔時間"
    )

    def handle(self, *args, **options):
        ROUND_START_HOUR = 14  # 回合開始時間-小時
        ROUND_START_MINUTE = 0  # 回合開始時間-分鐘
        ROUND_PLAY_TIME = 30  # 回合時間長度-分鐘
        ROUND_GAP_TIME = 10  # 回合間隔時間-分鐘

        start_time = None
        end_time = None
        for i in range(1, 6):  # 生成 5 個回合

            if i == 1:
                # 第一個回合不去計算回合間隔時間
                start_time = datetime.datetime.combine(
                    date=datetime.date.today(),
                    time=datetime.time(
                        hour=ROUND_START_HOUR, minute=ROUND_START_MINUTE
                    ),
                )
                end_time = start_time + datetime.timedelta(minutes=ROUND_PLAY_TIME)

            else:
                start_time = end_time + datetime.timedelta(minutes=ROUND_GAP_TIME)
                end_time = start_time + datetime.timedelta(minutes=ROUND_PLAY_TIME)

            round = Round.objects.create(
                start_time=start_time, end_time=end_time, is_valid=False
            )

            round.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"成功建立回合{round.pk}-開始時間{round.start_time}-結束時間{round.end_time}"
                )
            )

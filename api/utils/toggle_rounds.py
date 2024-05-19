import datetime
from django.utils import timezone
from api.models import Round


def toggle_rounds():
    now = timezone.now()  # 使用 Django 的 timezone.now() 確保時間準確
    today = now.date()  # 獲取今天的日期
    rounds = Round.objects.all().order_by("start_time")  # 按照開始時間排序

    for round in rounds:
        # 將 TimeField 轉換為 datetime.datetime 對象
        start_datetime = timezone.make_aware(
            datetime.datetime.combine(today, round.start_time),
            timezone.get_current_timezone(),
        )
        end_datetime = timezone.make_aware(
            datetime.datetime.combine(today, round.end_time),
            timezone.get_current_timezone(),
        )
        if now >= start_datetime and now <= end_datetime:
            # 如果當前時間在該回合內，則標記為有效
            round.is_valid = True
        else:
            # 否則，標記為無效
            round.is_valid = False
        round.save()  # 保存更改

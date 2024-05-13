from django.db import models
from django.forms import ValidationError
from django.utils import timezone


class Submission(models.Model):
    def validate_range(value):  # 限制分數在 0~100 之間
        if not isinstance(value, int) or value < 0 or value > 100:
            raise ValidationError("Value must be an integer between 0 and 100.")

    status_option = [  # 狀態選項
        ("todo", "todo"),
        ("doing", "doing"),
        ("fail", "fail"),
        ("success", "success"),
    ]

    code = models.TextField(default="", verbose_name="程式碼")
    score = models.IntegerField(
        default=0, validators=[validate_range], verbose_name="分數"
    )
    status = models.CharField(
        max_length=255, choices=status_option, default="todo", verbose_name="狀態"
    )
    team = models.ForeignKey("Team", on_delete=models.CASCADE, verbose_name="隊伍")
    time = models.DateTimeField(default=timezone.now, verbose_name="時間")
    challenge = models.ForeignKey(
        "Challenge", on_delete=models.CASCADE, verbose_name="挑戰"
    )
    round = models.ForeignKey("Round", on_delete=models.CASCADE, verbose_name="回合")

    def __str__(self):
        return f"{self.team}-{self.time.time()}-{self.round}-分數:{self.score}"

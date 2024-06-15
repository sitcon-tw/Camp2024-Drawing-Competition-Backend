from django.db import models


def upload_to(instance, filename):
    return f"images/{filename}"


class Challenge(models.Model):
    difficulty_option = [
        ("easy", "easy"),
        ("normal", "normal"),
        ("hard", "hard"),
    ]

    title = models.CharField(max_length=255, null=False, default="題目標題")
    description = models.TextField()
    image_url = models.ImageField(
        upload_to=upload_to,
        null=False,
        default="images/default.png",
        verbose_name="題目圖片",
    )
    difficulty = models.CharField(
        max_length=255, choices=difficulty_option, default="easy", verbose_name="難度"
    )
    round_id = models.ForeignKey("Round", on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"題目:{self.id}-{self.description}"

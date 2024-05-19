from django.db import models

class Round(models.Model):
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"回合:{self.id}"

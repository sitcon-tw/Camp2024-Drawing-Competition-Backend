from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=4, unique=True, null=False)

    def __str__(self):
        return self.name

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Part(models.Model):
    name = models.CharField(max_length=256, verbose_name="零件名稱")
    number = models.BigIntegerField(verbose_name="零件數量")
    min_number = models.BigIntegerField(verbose_name="零件最少數量")
    warning = models.BooleanField(verbose_name="警告狀態")
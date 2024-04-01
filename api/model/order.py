import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Order(models.Model):
    order_number = models.CharField(max_length=256, verbose_name="訂單編號")
    description = models.CharField(max_length=256, verbose_name="訂單描述")
    status = models.CharField(max_length=256, verbose_name="訂單狀態")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="操作員工 ID")
    expected_date = models.DateTimeField(verbose_name="預計完成日期")
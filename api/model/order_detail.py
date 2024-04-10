import datetime

from api.model.order import Order
from api.model.part import Part
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class OrderDetail(models.Model):
    number = models.BigIntegerField(verbose_name="零件數量")
    part_id = models.ForeignKey(Part, on_delete=models.CASCADE, verbose_name="零件 ID",default=1)
    order_number = models.CharField(
        max_length=255, verbose_name="對應訂單", default="XXX-XXX-XXX"
    )

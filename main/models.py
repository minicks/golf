from django.db import models
from django.db.models.fields.related import ManyToManyField
from account.models import *

class Month(models.Model):
    month = models.CharField(max_length=200, blank=True, null=True)

class Day(models.Model):
    day = models.CharField(max_length=200, blank=True, null=True)
    remain_seat = models.IntegerField(blank=True, null=True)
    f_month = models.ForeignKey(Month, on_delete=models.CASCADE, blank=True, null=True)

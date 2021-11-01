from django.db import models

# Create your models here.

class StockData(models.Model):
    date                = models.CharField(max_length=20)
    value_high          = models.CharField(max_length=20)
    value_low           = models.CharField(max_length=20)
    value_market_open   = models.CharField(max_length=20)
    value_market_close  = models.CharField(max_length=20)
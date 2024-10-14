from django.db import models

# Create your models here.

class SensorData(models.Model):
    ph = models.FloatField()  # pH值
    tds = models.FloatField()  # TDS值
    tmp=models.FloatField() 
    timestamp = models.DateTimeField(auto_now_add=True)  # 数据接收时间

    def __str__(self):
        return f"pH: {self.ph}, TDS: {self.tds} at {self.timestamp}"


class StatusData(models.Model):
    refreshing=models.BooleanField(default=False)
    
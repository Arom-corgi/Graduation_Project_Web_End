from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Device(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_bind = models.BooleanField(default=False)  # 表示设备是否被绑定

    def __str__(self):
        return self.name

    class Meta:
        db_table = '设备'
        ordering = ['unique_id']
        verbose_name = '设备'
        verbose_name_plural = '设备'


class BindDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bind_devices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='bind_users')
    bind_time = models.DateTimeField(auto_now_add=True)  # 绑定时间

    def __str__(self):
        return f"{self.user.username} - {self.device.name}"

    class Meta:
        db_table = '绑定设备'
        unique_together = (('user', 'device'),)  # 用户和设备的组合必须是唯一的
        verbose_name = '绑定设备'
        verbose_name_plural = '绑定设备'


class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='data')
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.IntegerField(blank=True, null=True)  # 心率
    blood_oxygen = models.FloatField(blank=True, null=True)  # 血氧水平
    temperature = models.FloatField(blank=True, null=True)  # 温度
    blood_pressure = models.IntegerField(blank=True, null=True) # 血压
    # 可根据需要添加更多字段

    def __str__(self):
        return f"{self.device.name} Data at {self.timestamp}"

    class Meta:
        db_table = '设备数据'
        ordering = ['-timestamp']  # 最新的数据首先显示
        verbose_name = '设备数据'
        verbose_name_plural = '设备数据'


from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Device(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        # 定义数据库中的表名
        db_table = '设备'
        # 定义默认排序方式，这里以id升序为例
        ordering = ['unique_id']
        # 设定一个或多个字段的组合为唯一约束
        unique_together = (('unique_id', 'user'),)
        # 设定模型的可读名称，在 admin 界面等地方显示
        verbose_name = '设备'
        verbose_name_plural = '设备'

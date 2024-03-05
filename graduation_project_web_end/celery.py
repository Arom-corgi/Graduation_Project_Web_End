from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# 设置 Django 的默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduation_project_web_end.settings')

app = Celery('graduation_project_web_end')

# 从 Django 的设置文件中加载 Celery 配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中加载任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 配置周期性任务
app.conf.beat_schedule = {
    'periodic_check_connection': {
        'task': 'index.tasks.periodic_check_connection',
        'schedule': crontab(minute='*/5'),  # 每5分钟执行一次
    },
}
# app.conf.beat_schedule = {
#     'check-stomp-connection': {
#         'task': 'index.tasks.check_connection',
#         'schedule': crontab(minute='*/5'),  # 每5分钟执行一次
#     },
# }
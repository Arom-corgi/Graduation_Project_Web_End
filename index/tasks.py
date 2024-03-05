from celery import shared_task
# 从阿里云iot导入检查链接逻辑
from common.aliyuniot import conn, connect_and_subscribe


@shared_task
def check_connection():
    print('检查STOMP连接状态...')
    if not conn.is_connected():
        try:
            connect_and_subscribe(conn)
            print('连接到了STOMP')
        except Exception as e:
            print('Error reconnecting to STOMP:', e)


# 最新版不再使用@periodic_task装饰器
# @periodic_task(run_every=crontab(minute='*/1'))
@shared_task
def periodic_check_connection():
    # 周期性任务的逻辑
    check_connection()
    print("Periodic connection check executed.")

# encoding=utf-8
import json
import os
import django
import time
import hashlib
import hmac
import base64
from datetime import datetime, timezone
import stomp
import ssl
import schedule
import threading
# 阿里云使用os包，为了方便管理这里和setting一样使用django-environ
# import os
import environ
from graduation_project_web_end.settings import BASE_DIR

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduation_project_web_end.settings')
django.setup()

# 必须设置django环境之后才可以引入APP的models文件
from index.models import *

# 设置.env路径
env_file = BASE_DIR / '.env'
# 初始化环境变量
env = environ.Env()
# 读取.env文件
environ.Env.read_env(env_file=str(env_file))


def connect_and_subscribe(conn):
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考
    accessKey = env('accessKey')
    accessSecret = env('accessSecret')
    consumerGroupId = env('consumerGroupId')
    # iotInstanceId：实例ID。
    iotInstanceId = env('iotInstanceId')
    clientId = env('clientId')
    # 签名方法：支持hmacmd5，hmacsha1和hmacsha256。
    signMethod = "hmacsha1"
    timestamp = current_time_millis()
    # userName组装方法，请参见AMQP客户端接入说明文档。
    # 若使用二进制传输，则userName需要添加encode=base64参数，服务端会将消息体base64编码后再推送。具体添加方法请参见下一章节“二进制消息体说明”。
    username = clientId + "|authMode=aksign" + ",signMethod=" + signMethod \
               + ",timestamp=" + timestamp + ",authId=" + accessKey \
               + ",iotInstanceId=" + iotInstanceId \
               + ",consumerGroupId=" + consumerGroupId + "|"
    signContent = "authId=" + accessKey + "&timestamp=" + timestamp
    # 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
    password = do_sign(accessSecret.encode("utf-8"), signContent.encode("utf-8"))

    conn.set_listener('', MyListener(conn))
    conn.connect(username, password, wait=True)
    # 清除历史连接检查任务，新建连接检查任务
    schedule.clear('conn-check')
    schedule.every(1).seconds.do(do_check, conn).tag('conn-check')


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        # print('received a message "%s"' % frame.body)
        # 解析消息
        data = json.loads(frame.body)

        # 从消息中提取数据
        unique_id = data['iotId']
        blood_oxygen = data['items']['blood_oxygen']['value']
        temperature = data['items']['temperature']['value']
        heart_rate = data['items']['heart_rate']['value']
        blood_pressure = data['items']['blood_pressure']['value']
        timestamp = datetime.fromtimestamp(data['items']['heart_rate']['time'] / 1000.0, tz=timezone.utc)

        # 查找对应的设备实例
        try:
            device = Device.objects.get(unique_id=unique_id, is_bind=True)
            # 创建DeviceData实例存储数据
            DeviceData.objects.create(
                device=device,
                timestamp=timestamp,
                heart_rate=heart_rate,
                blood_oxygen=blood_oxygen,
                temperature=temperature,
                blood_pressure=str(blood_pressure)  # 假设血压字段是字符串类型
            )
            print(f"设备 {unique_id} 的数据存储成功")
        except Device.DoesNotExist:
            print(f"设备 {unique_id} 未被绑定或不存在")

    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')

    def on_connected(self, headers):
        print("successfully connected")
        conn.subscribe(destination='/topic/#', id=1, ack='auto')
        print("successfully subscribe")

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


def current_time_millis():
    return str(int(round(time.time() * 1000)))


def do_sign(secret, sign_content):
    m = hmac.new(secret, sign_content, digestmod=hashlib.sha1)
    return base64.b64encode(m.digest()).decode("utf-8")


# 检查连接，如果未连接则重新建连
def do_check(conn):
    print('check connection, is_connected: %s', conn.is_connected())
    if not conn.is_connected():
        try:
            connect_and_subscribe(conn)
        except Exception as e:
            print('disconnected, ', e)


# 定时任务方法，检查连接状态
def connection_check_timer():
    while 1:
        schedule.run_pending()
        time.sleep(60)


#  接入域名，请参见AMQP客户端接入说明文档。这里直接填入域名，不需要带amqps://前缀
conn = stomp.Connection([(env('conn'), 61614)], heartbeats=(0, 300))
conn.set_ssl(for_hosts=[(env('conn'), 61614)], ssl_version=ssl.PROTOCOL_TLS)

try:
    connect_and_subscribe(conn)
except Exception as e:
    print('connecting failed')
    raise e

# 异步线程运行定时任务，检查连接状态
thread = threading.Thread(target=connection_check_timer)
thread.start()

# 使用官方 Python 运行时作为父镜像
FROM python:3.11.2

# 设置工作目录
WORKDIR /usr/src/app

# 将当前目录内容复制到位于 /usr/src/app 的容器中
COPY . .

# 安装 requirements.txt 中指定的所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 为容器指定要运行的命令
CMD ["gunicorn", "graduation_project_web_end.wsgi:application", "--bind", "0.0.0.0:8000"]

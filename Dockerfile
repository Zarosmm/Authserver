FROM python:3.6

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
ENV DB_ENGINE "mysql"
ENV MYSQL_HOST "172.16.3.124"
ENV REDIS_HOST "172.16.3.124"
ENV BACKEND_DEPLOY_ADDRESS "http://172.16.3.124"

# 添加 Debian 清华镜像源
RUN echo \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free\
    > /etc/apt/sources.list

RUN apt-get update
RUN mkdir /app

WORKDIR /app
ADD . /app
# 安装库
RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
RUN python manage.py collectstatic --no-input

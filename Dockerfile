FROM python:3.8-slim

MAINTAINER chaos:life0531@foxmail.com

RUN mkdir /root/search_bot

ADD . /root/search_bot

WORKDIR /root/search_bot

COPY sources.list /etc/apt/

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/

RUN pip3 install pysocks -i https://pypi.douban.com/simple/

CMD ["python3", "main.py"]

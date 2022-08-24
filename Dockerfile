FROM ubuntu:latest

ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

RUN apt-get install -y default-jdk default-jre

RUN apt-get install -y python3-pip python3-dev

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip3 install --upgrade pip

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /workspace
WORKDIR /workspace

RUN pip install jpype1-py3 konlpy

ENV WSGIPath config/wsgi.py

COPY ./requirements.txt /code/requirements.txt

RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /code/
WORKDIR /code/

EXPOSE 8000

ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
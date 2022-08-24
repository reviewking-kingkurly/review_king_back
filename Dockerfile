# configuration source: https://hub.docker.com/r/theeluwin/ubuntu-konlpy/dockerfile
# basing on ubuntu OS
FROM ubuntu:latest

# apt init
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

# installing java jdk and java jre
RUN apt-get install -y default-jdk default-jre

# installing python3 and pip3
RUN apt-get install -y python3-pip python3-dev


RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip3 install --upgrade pip

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# timezone
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# make workspace
RUN mkdir -p /workspace
WORKDIR /workspace

# install konlpy dependencies: jpype, konlpy, with mecab module
RUN pip install jpype1-py3 konlpy

# WSGIPath settings and DJANGO_SETTINGS_MODULE for deployment
ENV WSGIPath config/wsgi.py

# copying local file into container's /code/ directory
COPY ./requirements.txt /code/requirements.txt

# python & Django configuration
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copying the rest of the files into container's /code/ directory
# container's working directory is /code/
COPY . /code/
WORKDIR /code/

#Exposing port to 8000
EXPOSE 8000

# CMD multiple commands using start.sh file
ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
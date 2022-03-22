FROM python:3.9

RUN apt-get update &&\
    pip install --upgrade pip &&\
    apt-get install -y python3.9-dev mc

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD src/requiremetns.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app/src
ENTRYPOINT /app/src/start_server.sh

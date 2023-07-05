FROM python:3.11-slim-bookworm

ENV APP_HOME /opt/docker/scripts
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt

RUN apt-get update \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir \
    --upgrade pip \
    -r requirements.txt

COPY . $APP_HOME/

ENTRYPOINT ["python", "$1"]

FROM python:latest

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

ARG WORKER_COUNT=8
ENV WORKER_COUNT=${WORKER_COUNT}
RUN echo "Using WORKER_COUNT=${WORKER_COUNT}"

COPY . /app

EXPOSE 8080 5678
RUN mkdir -p /app/Logs

#Non Root User Configuration
RUN addgroup --system --gid 10001 app_grp\
    && adduser --system --disabled-password --uid 10000 --shell /bin/sh --home /app/ --ingroup app_grp app\
    && chown -R 10000:10001 /app

USER 10000

ENV KITE_USER_ID='dsdsdsd'
ENV KITE_PASSWORD=''
ENV LOGGING_LEVEL_CRON='INFO'
ENV TZ="Asia/Kolkata"

CMD gunicorn --timeout 21600 --workers ${WORKER_COUNT} app:app --bind 0.0.0.0:8080
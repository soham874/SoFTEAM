FROM python:latest

ENV KITE_USER_ID=''
ENV KITE_PASSWORD=''
ENV LOGGING_LEVEL_CRON='INFO'
ENV TZ="Asia/Kolkata"

RUN pip install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8080
RUN mkdir -p /app/Logs

#Non Root User Configuration
RUN addgroup --system --gid 10001 app_grp \
    && adduser --system --disabled-password --uid 10000 --shell /sbin/nologin --home /app/ --ingroup app_grp app\
    && chown -R 10000:10001 /app

USER 10000


CMD ["gunicorn","--timeout","21600","--workers","8", "app:app", "--bind", "0.0.0.0:8080"]

# clear && docker build -t nse_analyser . && docker container rm nse_analyser && docker run --name nse_analyser -it -p 8080:8080 nse_analyser
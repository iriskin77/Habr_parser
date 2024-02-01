FROM python:3.10-slim

WORKDIR /parser

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn


COPY . .

EXPOSE 8080

RUN chmod a+x /parser/start.sh
RUN chmod a+x /parser/celery_worker.sh
RUN chmod a+x /parser/celery_beat.sh

ENTRYPOINT ["./start.sh"]

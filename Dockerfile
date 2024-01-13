FROM python:3.10-slim

WORKDIR /parser

COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8080

RUN chmod a+x /parser/start.sh
RUN chmod a+x /parser/celery_worker.sh

ENTRYPOINT ["./start.sh"]

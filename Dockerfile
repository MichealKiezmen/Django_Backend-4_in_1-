FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app
RUN chmod +x start-app.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/app/start-app.sh"]

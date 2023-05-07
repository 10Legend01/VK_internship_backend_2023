FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY service ./service

WORKDIR /app/service

RUN python manage.py makemigrations service
RUN python manage.py migrate service

ENV PYTHONPATH "${PYTHONPATH}:/app"
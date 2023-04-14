FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && celery -A Instagram worker -l info && celery -A Instagram beat -l info"]

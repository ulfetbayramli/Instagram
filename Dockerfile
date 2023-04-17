FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /code

# set display port to avoid crash
# Use the latest official RabbitMQ image
FROM rabbitmq:3.9.5

# Set the username and password for RabbitMQ
ENV RABBITMQ_DEFAULT_USER=rabbitmq
ENV RABBITMQ_DEFAULT_PASS=rabbitmq

# Expose the RabbitMQ ports
EXPOSE 5672 15672

# Copy the RabbitMQ configuration file
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# Set the configuration for RabbitMQ
RUN rabbitmq-plugins enable --offline rabbitmq_management && \
    rabbitmq-plugins enable --offline rabbitmq_mqtt && \
    rabbitmq-plugins enable --offline rabbitmq_web_stomp && \
    rabbitmq-plugins enable --offline rabbitmq_stomp && \
    rabbitmq-plugins enable --offline rabbitmq_consistent_hash_exchange

# Start RabbitMQ

ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["sh", "-c", "rabbitmq-server && python manage.py makemigrations && python manage.py migrate && celery -A Instagram worker -l info && celery -A Instagram beat -l info"]


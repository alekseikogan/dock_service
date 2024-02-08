FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY service /service

WORKDIR /service

# открываем порт
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

# создаст пользователя в операционнной системе
RUN adduser --disabled-password service-user

# пользователь под которым все команды будут выполняться
USER service-user

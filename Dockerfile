FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY service /service

WORKDIR /service

# открываем порт
EXPOSE 8000

# устанавливаем зависимость между БД и приложением (3 пакета)
RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

# создаст пользователя в операционнной системе
RUN adduser --disabled-password service-user

# пользователь под которым все команды будут выполняться
USER service-user

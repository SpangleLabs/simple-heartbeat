FROM tiangolo/meinheld-gunicorn-flask:python3.6-alpine3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV MODULE_NAME "heartbeat_server"
ENV VARIABLE_NAME "app"
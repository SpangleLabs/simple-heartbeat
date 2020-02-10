FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
VOLUME /config
EXPOSE 5000
CMD ["heartbeat_server.py"]

FROM python:3.10-slim

WORKDIR /app
COPY app.py .

RUN pip install cassandra-driver

CMD ["python", "app.py"]

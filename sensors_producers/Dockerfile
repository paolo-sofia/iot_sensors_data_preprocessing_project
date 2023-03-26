FROM python:3.11.2-slim-bullseye AS BASE

WORKDIR /app

COPY . /app/src/sensors_producers

RUN pip install -r /app/src/sensors_producers/requirements.txt

ENTRYPOINT ["python", "/app/src/sensors_producers/sensor_data_producers.py"]

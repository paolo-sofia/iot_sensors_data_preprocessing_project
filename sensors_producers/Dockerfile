FROM python:3.11.2-slim-bullseye AS BASE

WORKDIR /app

COPY sensors_producers/requirements.txt /app/sensors_producers/requirements.txt
RUN pip install -r /app/sensors_producers/requirements.txt

COPY src /app/src
COPY sensors_producers/configs /app/sensors_producers/configs
COPY sensors_producers/sensors /app/sensors_producers/sensors
COPY sensors_producers/main.py /app/main.py
COPY sensors_producers/__init__.py /app/sensors_producers/__init__.py

ENTRYPOINT ["python", "main.py"]

FROM python:3.11.2-slim-bullseye AS BASE

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.11.2-slim-bullseye AS BASE

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install -r /api/requirements.txt

COPY ./app /api/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
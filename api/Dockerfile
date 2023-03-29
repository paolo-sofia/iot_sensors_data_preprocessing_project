FROM python:3.9-bullseye AS BASE
USER root
WORKDIR /app
RUN printenv
RUN which python
RUN apt-get update
RUN apt install -y openjdk-11-jdk
RUN apt install -y openjdk-11-jre
RUN apt install -y curl mlocate git scala

RUN wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
RUN tar xvf spark-3.3.2-bin-hadoop3.tgz


RUN export SPARK_HOME=/app/spark-3.3.2-bin-hadoop3
RUN export PATH=$PATH:$SPARK_HOME/bin
RUN export SPARK_LOCAL_IP=localhost
RUN export PYSPARK_PYTHON=/usr/local/bin/python
RUN export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
ENV PATH=$PATH:/usr/lib/jvm/java-1.11.0-openjdk-amd64/bin/
ENV JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64/
ENV PYSPARK_PYTHON=python
COPY api/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src /app/src
COPY api/spark_streaming /app/spark_streaming
COPY api/main.py /app/main.py
COPY api/__init__.py /app/__init__.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
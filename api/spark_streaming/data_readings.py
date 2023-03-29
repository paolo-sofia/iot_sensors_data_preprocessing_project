import json
import logging
import os
from typing import Any, Dict

import pyspark.sql.functions as F
from pyspark import SparkConf
from pyspark.sql import DataFrame, DataFrameReader, SparkSession
from pyspark.sql.types import FloatType, StringType, StructType

from src.sensor_type import QueryOptions

KAFKA_TOPIC_NAME: str = "sensor_readings_topic"
KAFKA_BOOTSTRAP_SERVER: str = "broker:9092"
KAFKA_STARTING_OFFEST: str = "earliest"
SENSOR_ID: str = "id"
SENSOR_TYPE: str = "sensor_type"
QUERY: str = """
    SELECT 
        *
    FROM
        kafka_topic
    WHERE
        {}='{}'
    AND 
        timestamp > '{}'
    AND 
        timestamp <= '{}'
"""
GROUP_BY_VALUE = "value"
JSON_SCHEMA: StructType = StructType() \
    .add("id", StringType()) \
    .add("name", StringType()) \
    .add("sensor_type", StringType()) \
    .add("value", FloatType())

logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

global spark
global dataframe
spark: SparkSession
dataframe: DataFrameReader


def create_session_and_start_stream() -> None:
    """Init function the creates the spark session and starts the stream reading from the kafka topic"""
    global spark
    global dataframe
    import socket

    spark_conf = SparkConf()
    spark_conf.setAll(
        [
            ("spark.master",
             os.environ.get("SPARK_MASTER_URL", "spark://spark-master:7077"),
             ),
            ("spark.driver.host", socket.gethostbyname(socket.gethostname())),
            ("spark.submit.deployMode", "client"),
            ("spark.driver.bindAddress", "0.0.0.0"),
            ("spark.driver.port", "8081"),
            ("spark.app.name", 'SparkKafkaSensorsDataManipulation'),
            ("spark.jars.packages",
             "org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,"
             "org.apache.kafka:kafka-clients:2.8.1")
        ]
    )

    spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    dataframe = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .option("startingOffsets", KAFKA_STARTING_OFFEST) \
        .load()
    return


def compute_data_statistics(sensor_name: str, sensor_type: str, start_datetime: str, end_datetime: str) \
        -> Dict[str, Any]:
    """
    Main function used when an api call is made. It fetches the data filtering by the values passed as parameters
    and computes some statistics about them (average value, min value, max value etc...) and returns the data as a json
    string
    :param sensor_name: the sensor name or family sensor name to get the data
    :param sensor_type: the type of sensor (sensor or family_sensor)
    :param start_datetime: the start time frame in which to fetch the data from
    :param end_datetime: the start time frame in which to fetch the data to
    :return: the computed data formatted as a json string
    """
    global spark
    global dataframe

    df: DataFrame = dataframe.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")
    df = df.withColumn("value", F.from_json("value", JSON_SCHEMA))
    df = df.select(["key", "timestamp", "value.*"])

    try:
        group_by_key = SENSOR_ID if sensor_type == QueryOptions.SENSOR else SENSOR_TYPE
        query: str = QUERY.format(group_by_key, sensor_name, start_datetime, end_datetime)

    except Exception as e:
        logger.error(f"{e}")
        return {}

    streaming_query = df.writeStream \
        .format("memory") \
        .queryName("kafka_topic") \
        .option('truncate', 'false') \
        .trigger(once=True) \
        .outputMode("append") \
        .start() \
        .awaitTermination()

    df_filtered = spark.sql(query)

    df_filtered = df_filtered.groupBy(group_by_key).agg(
        F.count(GROUP_BY_VALUE).alias("Number of readings"),
        F.avg(GROUP_BY_VALUE).alias("Average Value"),
        F.percentile_approx(GROUP_BY_VALUE, 0.5).alias('Median Value'),
        F.min(GROUP_BY_VALUE).alias("Min Value"),
        F.max(GROUP_BY_VALUE).alias("Max Value")
    )

    response: Dict[str, Any] = json.loads(df_filtered.toPandas().to_json())

    del df, df_filtered
    return response

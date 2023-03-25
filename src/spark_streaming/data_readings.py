from pyspark.sql import SparkSession
from datetime import datetime
from src.sensors.sensor_type import QueryOptions

KAFKA_TOPIC_NAME = "SAMPLE_TOPIC_NAME"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"

SENSOR_QUERY = """
    SELECT 
        *
    FROM
        df
    WHERE
        id='{}'
"""
SENSOR_FAMILY_QUERY = """
    SELECT 
        *
    FROM
        df
    WHERE
        sensor_type='{}'
"""


def compute_data_statistics(sensor_name: str, sensor_type: str, start_datetime: datetime, end_datetime: datetime):
    spark = (
        SparkSession.builder.appName("Kafka Pyspark Streaming Learning")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    dataframe = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)\
        .option("subscribe", KAFKA_TOPIC_NAME)\
        .option("startingOffsets", "earliest")\
        .load()

    dataframe.createTempView("kafka_topic")
    if sensor_type == QueryOptions.SENSOR:
        df = spark.sql("SELECT * FROM kafka_topic")
    else:
        df = spark.sql("SELECT * FROM kafka_topic")

    return df

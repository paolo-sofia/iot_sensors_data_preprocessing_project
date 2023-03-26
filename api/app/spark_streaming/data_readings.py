from datetime import datetime

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from src.sensor_type import QueryOptions

KAFKA_TOPIC_NAME: str = "SAMPLE_TOPIC_NAME"
KAFKA_BOOTSTRAP_SERVER: str = "localhost:9092"
SENSOR_ID: str = 'id'
SENSOR_TYPE: str = 'sensor_type'
QUERY: str = """
    SELECT 
        *
    FROM
        df
    WHERE
        {}='{}'
    AND 
        timestamp > {}
    AND 
        timestamp <= {}
"""


def compute_data_statistics(sensor_name: str, sensor_type: str, start_datetime: datetime, end_datetime: datetime):
    spark = SparkSession.builder.appName("Kafka Pyspark Streaming Learning") \
        .master("local[*]") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    dataframe = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .option("startingOffsets", "earliest") \
        .load()

    dataframe.createTempView("kafka_topic")
    if sensor_type == QueryOptions.SENSOR:
        df = spark.sql(QUERY.format(SENSOR_ID, sensor_name, start_datetime, end_datetime))
        group_by_key = "value"
    else:
        df = spark.sql(QUERY.format(SENSOR_TYPE, sensor_name, start_datetime, end_datetime))
        group_by_key = "type"

    return df.groupBy("department").agg(
        F.count(group_by_key).alias("count_value"),
        F.avg(group_by_key).alias("average_value"),
        F.percentile_approx(group_by_key, 0.5).alias('median_value'),
        F.min(group_by_key).alias("min_value"),
        F.max(group_by_key).alias("max_value")
    ).toJSON()

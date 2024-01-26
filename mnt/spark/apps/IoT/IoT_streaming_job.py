from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql import functions as func
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# DATASOURCE SETTTING

DATA_SOURCE = "IoT"
TABLE_NAME = 'temp&humd'

# KAFKA SETTING
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_SUBSCRIBE_TOPIC = "khang_topic"

# PATH
PREFIX_PATH = f"/data/{DATA_SOURCE}/{TABLE_NAME}"
# temporary storage
STREAMING_PATH = f"{PREFIX_PATH}/streaming/"

schema = StructType() \
    .add("temp", DoubleType()) \
    .add("humd", DoubleType()) \
    .add("time_stamp", StringType())


def read_message_kafka() -> DataFrame:
    try:
        message_reader = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
            .option("subscribe", KAFKA_SUBSCRIBE_TOPIC) \
            .load()

        return message_reader
    except Exception as e:
        raise Exception(f"Error in read_message_kafka: {e}")
    
def parse_messages(message_reader) -> DataFrame:
    try:
        parsed_df = message_reader.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", schema).alias("data")) \
            .select("data.temp", "data.humd", "data.time_stamp")

        return parsed_df
    except Exception as e:
        raise Exception(f"Error in read_message_kafka: {e}")
    

   
def writer_message_kafka(parsed_df: DataFrame) -> StreamingQuery:
    try:
        # consider the way of that kafka encode messages
        message_writer = parsed_df \
            .writeStream \
            .format("delta") \
            .option("path", STREAMING_PATH + "/raw/message") \
            .option("checkpointLocation", STREAMING_PATH + "/raw/checkpoint") \
            .outputMode("append") \
            .start()
        return message_writer
    except Exception as e:
        raise Exception(f"Error in writer_message_kafka: {e}")
    
def main():
    message_reader = read_message_kafka()

    message_writer = writer_message_kafka(message_reader)

    message_writer.awaitTermination()


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("IoT_streaming") \
        .getOrCreate()

    main()
    spark.stop()
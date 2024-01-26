from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql import functions as func
from ..utils import schemas
import mongodb_residentinfo_cdc as change_data_feed

#############################################
############### GLOBAL VARIABLES ############
#############################################

# DATABASE SETTTING
DBMS = "mongodb"
DATABASE_NAME = 't-building'
TABLE_NAME = "ResidentInfo"

# KAFKA SETTING
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_SUBSCRIBE_TOPIC = f"dbserver-{DBMS}.{DATABASE_NAME}.{TABLE_NAME}"

# PATH
PREFIX_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}"
# temporary storage
STREAMING_PATH = f"{PREFIX_PATH}/streaming/"


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


def writer_message_kafka(message_reader: DataFrame) -> StreamingQuery:
    try:
        # consider the way of that kafka encode messages
        message_writer = message_reader.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
            .writeStream \
            .format("json") \
            .option("path", STREAMING_PATH + "/raw/message") \
            .option("checkpointLocation", STREAMING_PATH + "/raw/checkpoint") \
            .outputMode("append") \
            .start()
        return message_writer
    except Exception as e:
        raise Exception(f"Error in writer_message_kafka: {e}")


def transform(message_reader: DataFrame):
    # consider use persist() function when deploy on cluster
    source_df = message_reader \
        .select(func.get_json_object(func.col("key").cast("string"), "$.payload.id")
                .alias('_id'),
                func.get_json_object(
                    func.col("value").cast("string"), "$.payload")
                .alias('payload')) \
        .withColumn("id", func.get_json_object(func.col("_id"), "$.$oid")) \
        .na.drop() \
        .withColumn("before", func.get_json_object(func.col("payload"), "$.before")) \
        .withColumn("after", func.get_json_object(func.col("payload"), "$.after")) \
        .withColumn("timestamp", func.get_json_object(func.col("payload"), "$.ts_ms")) \
        .withColumn("transaction",
                    func.when(func.col("before").isNull() & func.col("after").isNull(), "delete") \
                    .otherwise("none")) \
        .withColumn("data",
                    func.when(func.col("transaction") == 'none', func.col("after")) \
                    .otherwise(func.lit("None"))) \
        .withColumn("parser_data",
                    func.from_json(col=func.col("data"), schema=schemas.mongodb_Resident_Info).alias("data")) \
        .select("parser_data.*", "timestamp", "transaction", "id")

    change_data_feed.merge_tables_by_conditions(source_df, spark)


def transform_message_from_kafka(message_reader: DataFrame) -> StreamingQuery:
    transform_writer = message_reader.select("*") \
        .writeStream \
        .option("checkpointLocation", STREAMING_PATH + "/transform/checkpoint") \
        .trigger(processingTime='5 seconds') \
        .foreachBatch(lambda batch_df, _: transform(batch_df)) \
        .start()
    return transform_writer


def main():
    message_reader = read_message_kafka()

    message_writer = writer_message_kafka(message_reader)
    transform_mess_writer = transform_message_from_kafka(message_reader)

    transform_mess_writer.awaitTermination()
    message_writer.awaitTermination()


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("dev_streaming") \
        .getOrCreate()

    main()
    spark.stop()

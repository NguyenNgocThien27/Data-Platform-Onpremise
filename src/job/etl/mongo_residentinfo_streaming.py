from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import *
import json
import subprocess
import argparse
from datetime import datetime

#############################################
############### GLOBAL VARIABLES ############
#############################################

current_datetime = datetime.now().strftime("%y-%m-%d %H:%M:%S")
TABLE_NAME = "residentinfo"

# KAFKA SETTING
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_SUBSCRIBE_TOPIC = "dbserver-mongodb.t-building.ResidentInfo"

# MESSAGE STORAGE SETTING
MESSAGE_PATH = "/data/raw_layler/residentinfo/cdc/message/"
MESSAGE_CHECKPOINT_LOCATION = "/data/raw_layler/residentinfo/cdc/checkpoint/"

# temporary storage
TEMP_PATH = f"/data/raw_layler/residentinfo/cdc/"


# spark-submit setting
SPARK_SUBMIT_CMD = "spark-submit \
                    --master local[3] \
                    --driver-memory 1G --executor-memory 1G \
                    --packages io.delta:delta-core_2.12:2.1.0 \
                    /opt/spark-apps/etl/mongo_residentinfo_bronze_processing.py"

# SCHMEA DEFINE
RESIDENTINFO_SCHEMA = StructType([
    StructField("Action", StringType(), nullable=True),
    StructField("Address", StringType(), nullable=True),
    StructField("Apartments", ArrayType(StructType([
        StructField("block", StringType(), nullable=True),
        StructField("role", StringType(), nullable=True),
        StructField("floor", StringType(), nullable=True),
        StructField("room", StringType(), nullable=True)
    ])), nullable=True),
    StructField("AppToken", StructType([
        StructField("OS", StringType(), nullable=True),
        StructField("Token", StringType(), nullable=True)
    ]), nullable=True),
    StructField("Approval", StringType(), nullable=True),
    StructField("ApproveStatus", StringType(), nullable=True),
    StructField("ApprovedTime", StringType(), nullable=True),
    StructField("Approver", StringType(), nullable=True),
    StructField("ApproverEmail", StringType(), nullable=True),
    StructField("AuthyID", StringType(), nullable=True),
    StructField("Avatar", StringType(), nullable=True),
    StructField("BirthPlace", StringType(), nullable=True),
    StructField("Birthday", StringType(), nullable=True),
    StructField("BlockNumber", StringType(), nullable=True),
    StructField("Building", StringType(), nullable=True),
    StructField("CMND", StringType(), nullable=True),
    StructField("CMNDNote", StringType(), nullable=True),
    StructField("Career", StringType(), nullable=True),
    StructField("CreatedTime", StringType(), nullable=True),
    StructField("District", StringType(), nullable=True),
    StructField("Email", StringType(), nullable=True),
    StructField("FaceID", ArrayType(StringType()), nullable=True),
    StructField("FaceIdCount", StringType(), nullable=True),
    StructField("Floor", StringType(), nullable=True),
    StructField("FullName", StringType(), nullable=True),
    StructField("IssueDate", StringType(), nullable=True),
    StructField("IssuePlace", StringType(), nullable=True),
    StructField("Mask", StringType(), nullable=True),
    StructField("Method", StringType(), nullable=True),
    StructField("Nation", StringType(), nullable=True),
    StructField("Nationality", StringType(), nullable=True),
    StructField("Note", StringType(), nullable=True),
    StructField("NumberID", StringType(), nullable=True),
    StructField("OTP", StructType([
        StructField("ExpirationTime", StringType(), nullable=True),
        StructField("Token", StringType(), nullable=True)
    ]), nullable=True),
    StructField("Password", StringType(), nullable=True),
    StructField("Phone", StringType(), nullable=True),
    StructField("PrivateKey", StringType(), nullable=True),
    StructField("Province", StringType(), nullable=True),
    StructField("ReceivingCalls", StringType(), nullable=True),
    StructField("RegistrationType", StringType(), nullable=True),
    StructField("ResidenceRole", StringType(), nullable=True),
    StructField("ResidenceStatus", StringType(), nullable=True),
    StructField("Room", StringType(), nullable=True),
    StructField("Sex", StringType(), nullable=True),
    StructField("SigningKey", StringType(), nullable=True),
    StructField("SubAccount", BooleanType(), nullable=True),
    StructField("SyncStatus", BooleanType(), nullable=True),
    StructField("Temp", StringType(), nullable=True),
    StructField("Username", StringType(), nullable=True),
    StructField("Ward", StringType(), nullable=True),
    StructField("_id", StringType(), nullable=True),
    StructField("areaPolicy", ArrayType(StructType([
        StructField("areaName", StringType(), nullable=True),
        StructField("areaID", StringType(), nullable=True)
    ])), nullable=True),
    StructField("badgeId", StringType(), nullable=True),
    StructField("blockPermissions", ArrayType(StructType([
        StructField("block", StringType(), nullable=True),
        StructField("id", StringType(), nullable=True)
    ])), nullable=True),
    StructField("cmndIssuedDate", StringType(), nullable=True),
    StructField("dataTest", StringType(), nullable=True),
    StructField("deletedTime", StringType(), nullable=True),
    StructField("effectiveDate", StringType(), nullable=True),
    StructField("expiredDate", StringType(), nullable=True),
    StructField("expiryDate", StringType(), nullable=True),
    StructField("isAddedUnified", BooleanType(), nullable=True),
    StructField("isReceiveNotification", BooleanType(), nullable=True),
    StructField("isResident", BooleanType(), nullable=True),
    StructField("isStaff", BooleanType(), nullable=True),
    StructField("prevStatus", StringType(), nullable=True),
    StructField("reason", StringType(), nullable=True),
    StructField("syncFailure", ArrayType(StringType()), nullable=True),
    StructField("userId", StringType(), nullable=True),
    StructField("timestamp", StringType(), nullable=True),
    StructField("transaction", StringType(), nullable=True)
])

def get_current_timestamp():
    return int(datetime.timestamp(datetime.now()))

# parser = argparse.ArgumentParser()
# parser.add_argument("--source_path", help="source path", required=True)
# source_path = parser.parse_args().source_path

def read_message_kakfa():
    message_reader = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_SUBSCRIBE_TOPIC) \
        .load()
    
    return message_reader

def write_message_hdfs(message_reader):
    message_writer = message_reader.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream \
        .format("parquet") \
        .option("path", MESSAGE_PATH) \
        .option("checkpointLocation", MESSAGE_CHECKPOINT_LOCATION) \
        .outputMode("append") \
        .start()
    
    return message_writer

def write_message_console(message_reader)-> StreamingQuery:
    message_writer = message_reader.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream \
        .format("console") \
        .option("truncate", "false") \
        .outputMode("complete") \
        .start()
    
    return message_writer

def get_records(payload_list):
    records = []
    for payload in payload_list:
        record = json.loads(payload['after'])
        record['_id'] = record['_id']['$oid']
        record['timestamp'] = payload['ts_ms']
        if payload['updateDescription'] is not None:
            record['transaction'] = 'update'
        else:
            record['transaction'] = 'insert'
        records.append(record)
    return records

def trigger_jobs():
    subprocess.Popen(SPARK_SUBMIT_CMD.split())

def transform(df:DataFrame, path:str):
    rows = df.rdd.collect()
    payload_list = [json.loads(row.asDict()['value'])['payload'] for row in rows]
    records = get_records(payload_list)
    cdc_df = spark.createDataFrame(data=records, schema=RESIDENTINFO_SCHEMA)
    cdc_df.write.format("parquet").mode("overwrite").save(path)
    # trigger_jobs()

def transform_message(message_reader):
    path = TEMP_PATH + get_current_timestamp()
    transform_writer = message_reader.selectExpr("CAST(value AS STRING)") \
    .writeStream \
        .option("checkpointLocation", path + "/checkpoint") \
        .trigger(processingTime='1 minute') \
        .foreachBatch(lambda batch_df, _: transform(batch_df, path)) \
        .start()
    
    return transform_writer

def main():
    message_reader = read_message_kakfa()

    # message_writer = write_message_console(message_reader)
    message_writer = write_message_hdfs(message_reader)
    # transform_writer = transform_message(message_reader)

    # transform_writer.awaitTermination()
    message_writer.awaitTermination()


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("residentinfo_streaming") \
        .getOrCreate()

    main()
    spark.stop()
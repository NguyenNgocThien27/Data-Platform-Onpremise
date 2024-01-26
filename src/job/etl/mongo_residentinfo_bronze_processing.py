from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.window import Window
from pyspark.sql import DataFrame
import delta


# GLOBAL VARIABLES

DBMS = "mongodb"

TABLE_NAME = "residentinfo"

SOURCE_PATH = "/data/streaming/transform"

TARGET_PATH = "/data/mongodb/t-building/residentinfo/bronze/delta"

# CDC CONDITIONS
MATCHING_CONDITIONS = "target._id = source._id"
UPDATE_CONDITIONS = "target.timestamp < source.timestamp"

# SELECTED_COLUMNS = ['userId', 'Action', 'Address', 'Apartments', 'ApprovedTime', 'Approver', 'ApproverEmail',
#                     'ApproveStatus', 'AuthyID', 'Avatar', 'badgeId', 'Birthday', 'Career', 'CMND', 'CMNDNote',
#                     'CreatedTime', 'District', 'Email', 'FaceID', 'FullName', 'isAddedUnified',
#                     'isReceiveNotification', 'isStaff', 'IssueDate', 'IssuePlace', 'Nationality', 'Note',
#                     'Password', 'Phone', 'Province', 'reason', 'RegistrationType', 'ResidenceStatus', 'Sex',
#                     'SubAccount', 'Username', 'Ward']

def extract():
    try:
        raw_df = spark.read.format("delta").load(SOURCE_PATH)
        return raw_df
    except Exception as e:
        print("####################extract####################")

def transform(raw_df: DataFrame) -> DataFrame:
    try:
        bronze_df = raw_df.withColumn("timestamp", func.lit(func.unix_timestamp(func.current_timestamp()))) \
                          .withColumn("transaction", func.lit("insert"))
        return bronze_df
    except Exception as e:
        print("####################transform####################")

def load(bronze_df: DataFrame) -> None:
    try:
        bronze_df.write.format("delta").mode("overwrite").save(TARGET_PATH)
    except Exception as e:
        print("####################load####################")

def main():
    if not delta.DeltaTable.isDeltaTable(spark, TARGET_PATH):
        try:
            raw_df = extract()
            bronze_df = transform(raw_df)
            load(bronze_df)
            return True
        except:
            return False
    else:
        try:
            target_df = delta.DeltaTable.forPath(spark, TARGET_PATH)
            cdc_df = spark.read.format("parquet").load(SOURCE_PATH) \
                        .withCoumn
            target_df.alias('target') \
            .merge( \
                cdc_df.alias('source'), \
                MATCHING_CONDITIONS \
            ) \
            .whenMatchedUpdateAll(condition=UPDATE_CONDITIONS) \
            .whenNotMatchedInsertAll() \
            .execute()
            return True
        except:
            return False
        

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("MONGO_RESIDENTINFO_BROZNE_LAYER") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    if main():
        print("##########################")
        print("#                        #")
        print("#        DONE            #")
        print("#                        #")
        print("##########################")
    else:
        print("##########################")
        print("#                        #")
        print("#        ERROR           #")
        print("#                        #")
        print("##########################")
    spark.stop()




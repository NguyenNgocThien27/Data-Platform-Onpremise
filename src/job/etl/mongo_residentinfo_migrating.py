from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from delta.tables import *
from pyspark.sql import DataFrame
from datetime import datetime

current_datetime = datetime.now().strftime("%y-%m-%d %H:%M:%S")

# parser = argparse.ArgumentParser()

# # parser.add_argument("--source_path", help="source path")
# # parser.add_argument("--target_path", help="target path")
# parser.add_argument("--database", help="database name", required=True)
# parser.add_argument("--collection", help="collection name", required=True)

# args = parser.parse_args()
# if args.database:
#     database = args.database
# if args.collection:
#     collection = str(args.collection).lower()


# GOBAL VARIABLES

DBMS = "mongodb"

TARGET_PATH = f"/data/raw_layler/residentinfo/full_load_{current_datetime}"

# 172.22.0.4 is the IP address of the mongo container
MONGO_URI = f"mongodb://172.22.0.4:27017/t-building.ResidentInfo"

SELECTED_COLUMNS = ['userId', 'Action', 'Address', 'Apartments', 'ApprovedTime', 'Approver', 'ApproverEmail',
                    'ApproveStatus', 'AuthyID', 'Avatar', 'badgeId', 'Birthday', 'Career', 'CMND', 'CMNDNote',
                    'CreatedTime', 'District', 'Email', 'FaceID', 'FullName', 'isAddedUnified',
                    'isReceiveNotification', 'isStaff', 'IssueDate', 'IssuePlace', 'Nationality', 'Note',
                    'Password', 'Phone', 'Province', 'reason', 'RegistrationType', 'ResidenceStatus', 'Sex',
                    'SubAccount', 'Username', 'Ward']

def extract() -> DataFrame:
    try:
        mongo_df = spark.read.format("mongodb").load()
        return mongo_df
    except Exception as e:
        raise (e, "extract")

def transform(mongo_df: DataFrame) -> DataFrame:
    try:
        mongo_df = mongo_df.select(*[func.col(column_name) for column_name in SELECTED_COLUMNS])
        return mongo_df
    except Exception as e:
        raise (e, "transform")

def load(mongo_df: DataFrame):
    try:
        mongo_df.write.format("delta").mode("overwrite").save(TARGET_PATH)
    except Exception as e:
        raise (e, "load")

def main():
    try:
        mongo_df = extract()
        mongo_df = transform(mongo_df)
        load(mongo_df)
        return True
    except:
        return False

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("MONGO_MIGRATING") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.mongodb.read.connection.uri", MONGO_URI) \
        .getOrCreate()
    if main():
        print("####################################################")
        print("#-------------Migrating successfully--------------#")
        print("####################################################")
    else:
        print("####################################################")
        print("#-------------Migrating unsuccessfully------------#")
        print("####################################################")
        
    spark.stop()
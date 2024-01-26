from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from delta.tables import *
from pyspark.sql import DataFrame

SELECTED_COLUMNS = ['userId', 'Action', 'Address', 'Apartments', 'ApprovedTime', 'Approver', 'ApproverEmail',
                    'ApproveStatus', 'AuthyID', 'Avatar', 'badgeId', 'Birthday', 'Career', 'CMND', 'CMNDNote',
                    'CreatedTime', 'District', 'Email', 'FaceID', 'FullName', 'isAddedUnified',
                    'isReceiveNotification', 'isStaff', 'IssueDate', 'IssuePlace', 'Nationality', 'Note',
                    'Password', 'Phone', 'Province', 'reason', 'RegistrationType', 'ResidenceStatus', 'Sex',
                    'SubAccount', 'Username', 'Ward', "_id"]

DBMS = "mongodb"

DATABASE_NAME = 't-building'
TABLE_NAME = "residentinfo"

RAW_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/raw/delta"

BRONZE_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/bronze/delta"

SILVER_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/bronze/delta"


def extract(spark: SparkSession) -> DataFrame:
    try:
        mongo_df = spark.read.format(DBMS).load()
        return mongo_df
    except Exception as e:
        raise Exception(e, "extract")


def transform(mongo_df: DataFrame) -> DataFrame:
    try:
        mongo_df = mongo_df.select(*[func.col(column_name) for column_name in SELECTED_COLUMNS])
        mongo_df = mongo_df.withColumnRenamed("_id", "id")
        return mongo_df
    except Exception as e:
        raise Exception(e, "transform")


def load(mongo_df: DataFrame):
    try:
        mongo_df.write.format("delta").mode("overwrite").save(RAW_PATH)
    except Exception as e:
        raise Exception(e, "load")


def process_Migration(spark: SparkSession):
    try:
        mongo_df = extract(spark)
        bronze_df = transform(mongo_df)
        load(bronze_df)
    except Exception as e:
        msg = f"Something went wrong in migrating program - {e}"
        raise Exception(msg, e)

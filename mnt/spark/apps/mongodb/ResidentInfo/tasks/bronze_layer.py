from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql import DataFrame

DBMS = "mongodb"

DATABASE_NAME = 't-building'
TABLE_NAME = "residentinfo"

RAW_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/raw/delta"

BRONZE_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/bronze/delta"

SILVER_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/bronze/delta"


def extract(spark: SparkSession) -> DataFrame:
    try:
        raw_df = spark.read.format("delta").load(RAW_PATH)
        return raw_df
    except Exception as e:
        raise Exception(f"Error in extract: {e}")


def transform(raw_df: DataFrame) -> DataFrame:
    try:
        bronze_df = raw_df.withColumn("timestamp", func.lit(func.unix_timestamp(func.current_timestamp()))) \
            .withColumn("transaction", func.lit("insert")) \
            .withColumn("Birthday", func.to_date(func.col("Birthday")))
        return bronze_df
    except Exception as e:
        raise Exception(f"Error in transform: {e}")


def load(bronze_df: DataFrame) -> None:
    try:
        bronze_df.write.format("delta").mode("overwrite").save(BRONZE_PATH)
    except Exception as e:
        raise Exception(f"Error in load: {e}")


def process_Bronze(spark):
    try:
        raw_df = extract(spark)
        bronze_df = transform(raw_df)
        load(bronze_df)
    except Exception as e:
        msg = f"Something went wrong in bronze program - {e}"
        raise Exception(msg)

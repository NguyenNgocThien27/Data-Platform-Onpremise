import pyspark.sql.types as sql_type
import pyspark.sql.functions as func
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame

DBMS = "mongodb"

DATABASE_NAME = 't-building'
TABLE_NAME = "residentinfo"

RAW_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/raw/delta"

BRONZE_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/bronze/delta"

SILVER_PATH = f"/data/{DBMS}/{DATABASE_NAME}/{TABLE_NAME}/silver/delta"


@udf(returnType=sql_type.StringType())
def transform_sex(sex: str) -> str:
    try:
        sex = sex.lower()
        if sex == "male":
            return "Male"
        elif sex == 'female':
            return "Female"
        elif sex == 'other':
            return "Other"
    except:
        return sex


@udf(returnType=sql_type.StringType())
def transform_age_range(age: int) -> str:
    try:
        if age < 18:
            return "Under 18 years old"
        elif age <= 35:
            return "18 to 35 years old"
        elif age <= 55:
            return "36 to 55 years old"
        return "Over 55 years old"
    except:
        return age


def extract(spark: SparkSession):
    try:
        raw_df = spark.read.format('delta').load(BRONZE_PATH)
        return raw_df
    except Exception as e:
        raise Exception(f"Error in extract: {e}")


def transform(bronze_df: DataFrame):
    try:
        silver_df = bronze_df.withColumn("Age", func.year(func.current_date()) - func.year(func.col("Birthday"))) \
            .withColumn("Sex", transform_sex("Sex")) \
            .withColumn("age_range", transform_age_range(func.col("Age")))
        return silver_df
    except Exception as e:
        raise Exception(f"Error in transform: {e}")


def load(silver_df: DataFrame):
    try:
        silver_df.write.format("delta").mode("overwrite").save(SILVER_PATH)
    except Exception as e:
        raise Exception(f"Error in load: {e}")


def process_Silver(spark: SparkSession):
    try:
        bronze_df = extract(spark)
        silver_df = transform(bronze_df)
        load(silver_df)
    except Exception as e:
        msg = f"Something went wrong in silver program - {e}"
        raise Exception(msg)

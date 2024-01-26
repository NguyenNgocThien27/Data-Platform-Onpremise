import pyspark.sql.types as sql_type
import pyspark.sql.functions as func
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame
import delta
from datetime import datetime
from pyspark.sql.window import Window



# GLOBAL VARIABLES

DBMS = "mongodb"

TABLE_NAME = "residentinfo"

SOURCE_PATH = "/data/mongodb/t-building/residentinfo/bronze/delta"

TARGET_PATH = "/data/mongodb/t-building/residentinfo/silver/delta"

# CDC CONDITIONS
DELETING_CONDITIONS = ""
MATCHING_CONDITIONS = "target._id = source._id"
UPDATE_CONDITIONS = "target.timestamp < source.timestamp"


@udf(returnType=sql_type.StringType())
def transform_Sex(sex:str)->str:
    try:
        sex = sex.lower()
        if sex == "male":
            return "Male"
        elif sex == 'female':
            return "Female"
        elif sex == 'other':
            return "Other"
    except Exception:
        return sex
    
@udf(returnType=sql_type.StringType())
def transform_age_range(age:int) -> str:
    try:
        if age < 18:
            return "Under 18 years old"
        elif age <= 35:
            return "18 to 35 years old"
        elif age <= 55:
            return "36 to 55 years old"
        return "Over 55 years old"
    except Exception:
        return age

def extract()-> DataFrame:
    try:
        bronze_df = spark.read.format("delta").load(SOURCE_PATH)
        return bronze_df
    except Exception as e:
        print(e)

def transform(bronze_df):
    try:
        silver_df = bronze_df.withColumn("Birthday", func.to_date(func.col("Birthday"))) \
                            .withColumn("Age", func.year(func.current_date()) - func.year("Birthday")) \
                            .withColumn("Sex", transform_Sex("Sex")) \
                            .withColumn("age_range", transform_age_range("Age"))
        return silver_df
    except Exception as e:
        print(e)

def load(silver_df):
    try:
        silver_df.write.format("delta").mode("overwrite").save(TARGET_PATH)
    except Exception as e:
        print(e)

# def main():
#         spark.read.format("delta").load(SOURCE_PATH)\
#         .withColumn("Birthday", func.to_date(func.col("Birthday")))\
#         .withColumn("Age", func.year(func.current_date()) - func.year("Birthday"))\
#         .withColumn("Sex", transform_Sex("Sex"))\
#         .withColumn("age_range", transform_age_range("Age"))\
#         .write.format('delta').mode("overwrite").save(TARGET_PATH)


def main():
    if not delta.DeltaTable().isDeltaTable(TARGET_PATH):
        bronze_df = extract()
        silver_df = transform(bronze_df)
        load(silver_df)
    else:
        try:
            target_df = delta.DeltaTable.forPath(spark, TARGET_PATH)
            cdc_df = spark.read.format("delta").load(SOURCE_PATH)
            cdc_silver_df = transform(cdc_df)
            target_df.alias('target') \
            .merge( \
                cdc_silver_df.alias('source'), \
                MATCHING_CONDITIONS \
            ) \
            .whenMatchedUpdateAll(condition=UPDATE_CONDITIONS) \
            .whenNotMatchedInsertAll() \
            .execute()
            return True
        except:
            return False

if __name__ == "__main__":
    spark = SparkSession.builder.appName("MONGO_RESIDENTINFO_SILVER_LAYER")\
                .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
                .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate()
    main()
    spark.stop()
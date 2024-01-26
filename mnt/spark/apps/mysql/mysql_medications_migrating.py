from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql import DataFrame

LAYER = "migrating"
READ_FORMAT = "JDBC"
DBMS = "synthea"
TABLE_NAME = "medications"


def extract(spark: SparkSession) -> DataFrame:
    try:
        raw_df = spark.read \
            .format(READ_FORMAT) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("url", f"jdbc:mysql://192.168.195.84:3306/{DBMS}") \
            .option("dbtable", f"{TABLE_NAME}") \
            .option("user", "mysqluser") \
            .option("password", "mysqlpw") \
            .load()
        return raw_df
    except Exception as e:
        raise Exception(f"Error in extract function: {e}")


def transform(layer_df: DataFrame) -> DataFrame:
    pass


def load(raw_df: DataFrame) -> None:
    try:
        raw_df.write.format("delta").mode("overwrite").save("/data/mysql/healthcare/medications/delta")
    except Exception as e:
        raise Exception(f"Error in load function: {e}")


def process_Migrating(spark) -> None:
    try:
        raw_df = extract(spark)
        load(raw_df)
    except Exception as e:
        msg = f"Something went wrong in {LAYER} program - {e}"
        raise Exception(msg)


def initial_spark() -> SparkSession:
    return SparkSession.builder \
        .appName("appMinIO") \
        .getOrCreate()

if __name__ == "__main__":
    spark = initial_spark()
    process_Migrating(spark)
from pyspark.sql import SparkSession
import tasks


def main(spark: SparkSession):
    try:
        tasks.process_Migration(spark)
        tasks.process_Bronze(spark)
        tasks.process_Silver(spark)
        print("##################################")
        print("##################################")
        print("############## DONE ##############")
        print("##################################")
        print("##################################")
    except Exception as e:
        print("##################################")
        print("##################################")
        print(f"############## {e} ##############")
        print("##################################")
        print("##################################")


def initial_spark() -> SparkSession:
    return SparkSession.builder \
        .appName("appMinIO") \
        .getOrCreate()


if __name__ == "__main__":
    spark = initial_spark()
    main(spark)

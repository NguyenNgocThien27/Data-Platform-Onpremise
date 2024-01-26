from pyspark.sql import SparkSession
import medications as layers


def main(spark: SparkSession):
    try:
        layers.process_Migrating(spark)
        layers.process_Bronze(spark)
        layers.process_Silver(spark)
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

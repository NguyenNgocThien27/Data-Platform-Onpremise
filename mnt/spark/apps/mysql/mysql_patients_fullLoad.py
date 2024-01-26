from pyspark.sql import SparkSession
import Table_Patients as layer

def main(spark):
    try:
        layer.process_Migration(spark)
        layer.process_Bronze(spark)
        layer.process_Silver(spark)
        layer.process_Gold(spark)
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

def initial_spark():
    return SparkSession.builder \
            .appName("fullLoad_table_Patients") \
            .getOrCreate()

if __name__ == "__main__":
    spark = initial_spark()
    main(spark)
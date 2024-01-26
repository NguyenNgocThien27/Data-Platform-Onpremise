from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("fake")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate()
columns = ["language","users_count"]
data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
spark.createDataFrame(data=data, schema=columns).write.format("delta").save("/data/fake")
spark.stop()
sudo docker exec -it tdp-spark-master bin/bash opt/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.mongodb.spark:mongo-spark-connector_2.12:10.1.1,io.delta:delta-core_2.12:2.1.0 --conf "spark.mongodb.read.connection.uri=mongodb://192.168.96.2:27017/t-building.ResidentInfo" --conf  "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" --py-files opt/spark-apps/ResidentInfo.zip opt/spark-apps/mongodb/ResidentInfo/mongo_residentinfo_full_loading.py
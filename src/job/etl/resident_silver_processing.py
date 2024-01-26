from pyspark.sql import SparkSession
import pyspark.sql.types as sql_type
import pyspark.sql.functions as fun
from pyspark.sql.functions import udf

@udf(returnType=sql_type.StringType())
def transform_Sex(sex:str)->str:
    try:
        sex = sex.lower()
        if sex in ['nam', 'male']:
            return "Male"
        elif sex in ['nu', 'nữ', 'female']:
            return "Female"
        elif sex in ['other','khác']:
            return "Other"
        return None
    except Exception:
        return None
    
@udf(returnType=sql_type.StringType())
def transform_ResidentStatus(status:str)->str:
    try:
        status = status.lower()
        if status == 'rejected':
            return "Đã từ chối"
        elif status == 'deactivated':
            return "Đã hủy"
        elif status == 'active':
            return "Hoạt động"
        elif status == 'expired':
            return "Hết hạn"
        elif status == 'inactive':
            return "Vô hiệu hóa"
    except Exception as e:
        return None
    
@udf(returnType=sql_type.StringType())
def transform_Age_range(age:int) -> str:
    try:
        if age < 18:
            return "Under 18"
        elif age <= 35:
            return "18-35"
        elif age <= 50:
            return "36-50"
        return "Over 50"
    except Exception:
        return None

def main():
    try:
        spark.read.format("delta").load("/data/bronze/residentInfo/delta")\
        .withColumn("Birthday", fun.to_date("Birthday", format="yyyy-mm-dd"))\
        .withColumn("Age", fun.year(fun.current_date()) - fun.year("Birthday"))\
        .withColumn("Sex", transform_Sex("Sex"))\
        .withColumn("age_range", transform_Age_range("Age"))\
        .write.format('delta').mode("overwrite").save('/data/silver/residentInfo/delta')
        return True
    except :
        return False


if __name__ == "__main__":
    spark = SparkSession.builder.appName("bronze_layer")\
            .config("spark.sql.caseSensitive", "true")\
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate()
    if main():
        print("Done!")
    else:
        print("Error!")
    spark.stop()
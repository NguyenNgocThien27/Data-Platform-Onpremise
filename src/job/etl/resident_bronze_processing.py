from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import pyspark.sql.types as sql_type
import pyspark.sql.functions as fun
from pyspark.sql.functions import udf


def read_data_from_bronze():
    try:
        return spark.read.format("json")\
                            .load(path="file:///opt/spark-data/full_loads.json")\
                            .select(fun.explode("Items").alias("Items"))\
                            .select("Items.*")
        
    except Exception as e:
        return e

def check_type_can_process(columns_type_list:list) ->bool:
    for col_type in columns_type_list:
        if col_type in ['BOOL', "NULL", 'L', "M"]:
            return False
    return True

@udf(returnType=sql_type.BooleanType())
def change_string_to_boolean(value:str):
    try:
        if value.lower() in ['true','có', 'co', 'yes']:
            return True
        elif value.lower() in ['false','không', 'khong', 'no']:
            return False
    except AttributeError:
        return None

@udf(returnType=sql_type.StringType())
def change_boolean_to_string(value: bool) -> str:
    try:
        if value:
            return 'true'
        return 'false'
    except (AttributeError, ValueError):
        return None
    
@udf(returnType=sql_type.StringType())
def check_timestamp(value: str):
    try:
        return value if value.isdigit() else None
    except AttributeError:
        return None

@udf(returnType=sql_type.StringType())
def fill_empty_value(value:str) ->str:
    try:
        if value != None and len(value) == 0:
            return None
        return value
    except Exception as e:
        return None
    
def convert_S_type(dataframe, columnName):
    return dataframe.withColumn(colName=columnName,
                                     col=fun.col(f"{columnName}.S")
                                     .cast(sql_type.StringType()))

def convert_N_type(dataframe, column_Name):
    if 'Time' in column_Name:
        return dataframe.withColumn(colName=column_Name, col=fun.col(f"{column_Name}.N")
                                        .cast(sql_type.StringType()))
    else:
        return dataframe.withColumn(colName=column_Name, col=fun.col(f"{column_Name}.N")
                                        .cast(sql_type.IntegerType()))
    
def convert_BOOL_type(dataframe, column_Name, type_Column):
    return dataframe.withColumn(colName=column_Name, col=fun.col(f"{column_Name}.{type_Column}")
                                                    .cast(sql_type.BooleanType())) 

def convert_multiple_nested_columns(dataframe, column_Name, nested_columns_inside_column_list):
    nested_columns_inside_column_list = [column_Name + '.' + col for col in nested_columns_inside_column_list]
    return dataframe.withColumn(colName=column_Name, col=fun.coalesce(*nested_columns_inside_column_list))

def convert_complex_type(dataframe, columns_not_process: list=[]):
    columns_in_df = dataframe.columns
    for column_Name in columns_in_df:
        if column_Name not in columns_not_process:
            try:
                column_Dataframe = dataframe.select(f"{column_Name}.*")
                try:
                    nested_columns_inside_column_list = column_Dataframe.columns
                    if len(nested_columns_inside_column_list) == 1:
                        type_col = column_Dataframe.columns[0]
                        if type_col == 'S':  
                            dataframe = convert_S_type(dataframe, column_Name)
                        elif type_col == 'N':
                            dataframe = convert_N_type(dataframe, column_Name)
                        elif type_col in ['BOOL', 'NULL']:  
                            dataframe = convert_BOOL_type(dataframe, column_Name, type_col)    
                    elif check_type_can_process(nested_columns_inside_column_list):
                        dataframe = convert_multiple_nested_columns(dataframe, column_Name, nested_columns_inside_column_list)
                except Exception:
                    print(column_Name, 'change column')
            except Exception :
                print(column_Name, 'query')
    return dataframe

def upload_pendingInformation(pendingInfo_dataframe):
    try:
        convert_complex_type(pendingInfo_dataframe)\
                            .withColumn("block", fun.col("Apartments.L.M.block.S").alias('block'))\
                            .withColumn('floor', fun.col("Apartments.L.M.floor.S"))\
                            .withColumn('role',fun.col("Apartments.L.M.role.S"))\
                            .withColumn('room',fun.col("Apartments.L.M.room.S"))\
                            .withColumn("Apartments", fun.arrays_zip("block", "floor", "role", "room"))\
                            .withColumn('OS', fun.col("AppToken.M.OS.S"))\
                            .withColumn('Token', fun.col("AppToken.M.Token.S"))\
                            .withColumn('AppToken', fun.struct('OS', 'Token'))\
                            .withColumn("FaceID", fun.col("FaceID.L.S"))\
                            .drop("block",'floor', "role", 'room', 'OS', "Token")\
                            .write.format("delta").mode("overwrite").save("/data/bronze/pending_residentInfo/delta")
        return True
    except Exception as e:
        return False
    
def upload_ResidentInfo(residentInfo_dataframe):
    try:
        convert_complex_type(residentInfo_dataframe, ['pendingInformation.ApproveStatus', 'pendingInformation'])\
            .withColumn('OS', fun.col("AppToken.M.OS.S"))\
            .withColumn('Token', fun.col("AppToken.M.Token.S"))\
            .withColumn('AppToken', fun.struct('OS', 'Token'))\
            .withColumn("syncFailure", fun.col("syncFailure.L.S"))\
            .withColumn('FaceID', fun.col("FaceID.L.S"))\
            .withColumn('areaPolicy', fun.col("areaPolicy.L"))\
            .withColumn('ExpirationTime', fun.col("OTP.M.ExpirationTime.N").cast(sql_type.StringType()))\
            .withColumn('Token', fun.col('OTP.M.Token.S').cast(sql_type.StringType()))\
            .withColumn('OTP', fun.struct('ExpirationTime', 'Token'))\
            .withColumn('AuthyID', fun.col("AuthyID").cast(sql_type.StringType()))\
            .withColumn("block", fun.col("Apartments.L.M.block.S").alias('block'))\
            .withColumn('floor', fun.col("Apartments.L.M.floor.S"))\
            .withColumn('role',fun.col("Apartments.L.M.role.S"))\
            .withColumn('room',fun.col("Apartments.L.M.room.S"))\
            .withColumn("Apartments", fun.arrays_zip("block", "floor", "role", "room"))\
            .withColumn("block", fun.col("blockPermissions.L.M.block.S").alias('block'))\
            .withColumn('id', fun.col("blockPermissions.L.M.id.S"))\
            .withColumn("blockPermissions", fun.arrays_zip("block", "id"))\
            .withColumn('areaDescription', fun.col("areaPolicy.M.areaDescription.S"))\
            .withColumn('areaID', fun.col("areaPolicy.M.areaID.S"))\
            .withColumn('areaImage', fun.col("areaPolicy.M.areaImage.S"))\
            .withColumn('id', fun.col("areaPolicy.M.id.S"))\
            .withColumn('areaPolicy', fun.arrays_zip('areaDescription', 'areaID', 'areaImage', 'id'))\
            .withColumn('SubAccount', fun.coalesce(fun.col("SubAccount.BOOL"),change_string_to_boolean(fun.col("SubAccount.S"))))\
            .withColumn("effectiveDate", fun.col("effectiveDate.N"))\
            .withColumn("expiredDate", fun.coalesce(fill_empty_value(fun.col('expiredDate.S')), 
                                    change_boolean_to_string(fun.col("expiredDate.NULL"))))\
                .drop('pendingInformation', "pendingInformation.ApproveStatus",'areaDescription', 'areaID', 'areaImage', 'id'
                    "block", "id", "block", "floor", "role", "room", 'ExpirationTime','Token', 'OS','Token', "roominfo", "RoomInfo", "IsResident")\
                .write.format("delta").mode("overwrite").save("/data/bronze/residentInfo/delta")
        return True
    except Exception as e:
        return False
    

def main():
    try:
        dataframe = read_data_from_bronze()
        pending_dataframe = dataframe.select(fun.col("pendingInformation.M.*"),
                            fun.col("`pendingInformation.ApproveStatus`").alias("ApproveStatus"))
        if (upload_pendingInformation(pending_dataframe) and upload_ResidentInfo(dataframe)):
            return True
    except:
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


from delta.tables import *
from pyspark.sql.window import Window
from pyspark.sql import functions as func
from tasks import transform_to_silver


# from singleton import GlobalVariables


# Notes:
# - enable `change data feed`
# - all paths and variables what will be stored in class or .env file to clear and easy to maintain.
# - if u want to set specific variables that need to be updated,
#        pass dictionary object into delta lake functions
def merge(source_df: DataFrame, target_path: str, spark: SparkSession) -> None:
    """
    merging based on conditions that be provided
    :param source_df: source data frame
    :param target_path: the path that you want to get data frame
    :param spark: Spark Session
    :return:
    """
    resident_info_matching_conditions = 'source.id = destination.id'
    resident_info_update_conditions = 'source.timestamp > destination.timestamp'
    resident_info_delete_conditions = "source.transaction = 'delete'"

    target_df: DeltaTable = DeltaTable.forPath(spark, target_path)
    target_df.alias("destination") \
        .merge(
        source=source_df.alias("source"),
        condition=resident_info_matching_conditions) \
        .whenMatchedDelete(condition=resident_info_delete_conditions) \
        .whenMatchedUpdateAll(condition=resident_info_update_conditions) \
        .whenNotMatchedInsertAll() \
        .execute()


#
def get_newest_rows_df(source_df: DataFrame) -> DataFrame:
    """
    using window function to get the newest rows in the micro-batch data frame
    :param source_df:
    :return: data frame that contains the newest rows.
    """
    window_func = Window.partitionBy("userId").orderBy(func.col("timestamp").desc())
    newest_rows_df = source_df.withColumn("rank", func.rank().over(window_func)) \
        .where(func.col("rank") == 1) \
        .drop("rank")
    return newest_rows_df


def merge_tables_by_conditions(source_df: DataFrame, spark: SparkSession):
    try:
        source_df = get_newest_rows_df(source_df)
        paths = ["/data/mongodb/t-building/residentinfo/bronze/delta",
                 "/data/mongodb/t-building/residentinfo/silver/delta"]
        merge(source_df, paths[0], spark)
        transformed_silver_df = transform_to_silver(source_df)
        merge(transformed_silver_df, paths[1], spark)
    except Exception as e:
        raise Exception(f"Error in change_data_capture: {e}")

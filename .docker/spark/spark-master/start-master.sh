#!/bin/bash
# export SPARK_DIST_CLASSPATH=$($HADOOP_HOME/bin/hadoop --config $HADOOP_CONF_DIR classpath)
export SPARK_MASTER_HOST=`hostname`

. "$SPARK_HOME/sbin/spark-config.sh"

. "$SPARK_HOME/bin/load-spark-env.sh"

mkdir -p $SPARK_MASTER_LOG_DIR

ln -sf /dev/stdout $SPARK_MASTER_LOG_DIR/spark-master.out

$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_UI_PORT >> $SPARK_MASTER_LOG_DIR/spark-master.out

exec "$@"

# logs
# echo $SPARK_DIST_CLASSPATH
# echo $SPARK_MASTER_HOST
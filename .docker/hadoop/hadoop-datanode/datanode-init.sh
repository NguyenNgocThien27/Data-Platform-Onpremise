#!/bin/bash
# Remove "file://"
DATA_DIR=`echo $HDFS_CONF_DFS_DATANODE_DATA_DIR | perl -pe 's#file://##'`
# Check exists of NAME_DIR /hadoop/dfs/name
if [ ! -d $DATA_DIR ]; then
    echo "Namenode name directory not found: $DATA_DIR"
    exit 2
fi

$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR datanode
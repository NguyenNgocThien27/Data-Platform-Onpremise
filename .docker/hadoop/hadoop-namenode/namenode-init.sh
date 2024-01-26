#!/bin/bash
# Remove "file://"
NAME_DIR=`echo $HDFS_CONF_DFS_NAMENODE_DATA_DIR | perl -pe 's#file://##'`
# Check exists of NAME_DIR /hadoop/dfs/name
if [ ! -d $NAME_DIR ]; then
    echo "Namenode name directory not found: $NAME_DIR"
    exit 2
fi
# Check CLUSTER_NAME is empty
if [ -z "$CLUSTER_NAME" ]; then
    echo "Cluster name not specified"
    exit 2
fi

# The lost+found directory is not needed in this context, and removing it can be part of 
# a clean-up process to ensure that the namenode directory contains only the required files and directories.
echo "remove lost+found from $NAME_DIR"
rm -r $NAME_DIR/lost+found

# Format NameNode's file system will remove all data stored in HDFS
if [ "`ls -A $NAME_DIR`" == "" ]; then
    echo "Formatting namenode directory: $NAME_DIR"
    $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
fi

# Format NameNode's file system will remove all data stored in HDFS

# if [ "`ls -A $NAME_DIR`" != "" ]; then
#     echo "Formatted namenode directory: $NAME_DIR"
    
# fi

# SY
# if [ "`ls -A $NAME_DIR`" == "" ]; then
#     echo "Formatting namenode directory: $NAME_DIR"
#     $HADOOP_HOME/bin/hdfs -format namenode 
# fi

# $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode
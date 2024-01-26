FROM hadoop-base:latest
LABEL maintainer="ntlminh@tma.com.vn"

ENV HDFS_CONF_DFS_NAMENODE_DATA_DIR=file:///hadoop/dfs/name

RUN mkdir -p /hadoop/dfs/name

COPY namenode-init.sh namenode-init.sh

RUN chmod a+x ./namenode-init.sh

EXPOSE 9870

CMD [ "./namenode-init.sh" ]
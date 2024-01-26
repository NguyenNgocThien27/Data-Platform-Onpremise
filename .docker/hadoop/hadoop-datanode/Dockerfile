FROM hadoop-base:latest
LABEL maintainer="ntlminh@tma.com.vn"

ENV HDFS_CONF_DFS_DATANODE_DATA_DIR=file:///hadoop/dfs/data

RUN mkdir -p /hadoop/dfs/data

VOLUME /hadoop/dfs/data

COPY datanode-init.sh datanode-init.sh

RUN chmod a+x ./datanode-init.sh

EXPOSE 9864
# ENTRYPOINT [ "/bin/bash" ]
CMD [ "./datanode-init.sh" ]
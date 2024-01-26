FROM hive-base:latest
LABEL maintainer="ntlminh@tma.com.vn"

COPY hive-metastore-init.sh hive-metastore-init.sh

RUN chmod +x hive-metastore-init.sh

CMD [ "./hive-metastore-init.sh" ]
# ENTRYPOINT ["/bin/bash"]
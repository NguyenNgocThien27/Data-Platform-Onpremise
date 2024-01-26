FROM hadoop-base:latest
LABEL Minh="ntlminh@tma.com.vn"
LABEL Sy="pminhsy@tma.com.vn"
LABEL Thien="nnthien1@tma.com.vn"

ARG HIVE_VERSION
ENV HIVE_VERSION=${HIVE_VERSION:-3.1.2}
ENV HIVE_HOME=/opt/hive
ENV PATH=${HIVE_HOME}/bin:$PATH

WORKDIR /opt

RUN apt-get install -yqq \
    wget \
    procps

RUN wget --no-check-certificate -c -O hive.tar.gz https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz 
RUN tar xvf hive.tar.gz 
RUN rm hive.tar.gz 
RUN mv apache-hive-${HIVE_VERSION}-bin hive
RUN wget --no-check-certificate -O ${HIVE_HOME}/lib/postgresql-jdbc.jar https://jdbc.postgresql.org/download/postgresql-42.2.14.jar 
RUN wget --no-check-certificate -O ${HIVE_HOME}/lib/delta-hive-assembly_2.12-0.6.0.jar https://github.com/delta-io/connectors/releases/download/v0.6.0/delta-hive-assembly_2.12-0.6.0.jar 
# RUN apt-get --purge remove -yqq wget
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*

# Fix bug 1: classpath logging conflict. Class path contains multiple SLF4J bindings.
RUN rm /opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar 
# Fix bug 2: Exception in thread "main" java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument(ZLjava/lang/String;Ljava/lang/Object;)V
RUN rm ${HIVE_HOME}/lib/guava-19.0.jar
RUN cp ${HADOOP_HOME}/share/hadoop/hdfs/lib/guava-27.0-jre.jar ${HIVE_HOME}/lib
# Fix bug 3: Remove underscores.
# Spark should be compiled with Hive to be able to use it
# hive-site.xml should be copied to $SPARK_HOME/conf folder

COPY ./conf/hive-site.xml ${HIVE_HOME}/conf
COPY ./conf/hive-env.sh ${HIVE_HOME}/conf
COPY ./conf/ivysettings.xml ${HIVE_HOME}/conf

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 10000 
EXPOSE 10001
EXPOSE 10002

ENTRYPOINT [ "./entrypoint.sh" ]
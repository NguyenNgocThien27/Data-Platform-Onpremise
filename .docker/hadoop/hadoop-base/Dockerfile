FROM ubuntu:20.04
LABEL Minh="ntlminh@tma.com.vn"
LABEL Sy="pminhsy@tma.com.vn"
LABEL Thien="nnthien1@tma.com.vn"

# USER root

# Install dependencies & JAVA
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    apt-utils \
    curl \
    openjdk-8-jdk \
    wget \
    netcat && \
    apt-get autoremove -yqq --purge

# Setup JAVA
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
ENV PATH=${JAVA_HOME}/bin/:$PATH

# Setup HADOOP
ENV HADOOP_VERSION=3.2.1
ENV HADOOP_URL=https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV PATH=${HADOOP_HOME}/bin/:$PATH
ENV USER=root

# Download Hadoop file
RUN mkdir -p /opt/hadoop
RUN wget --no-check-certificate -c -O hadoop.tar.gz ${HADOOP_URL}
RUN tar xvf hadoop.tar.gz --directory=${HADOOP_HOME} --exclude=hadoop-${HADOOP_VERSION}/share/doc --strip 1 
RUN rm -rf hadoop.tar.gz 
RUN ln -s ${HADOOP_HOME}/etc/hadoop ${HADOOP_CONF_DIR}
RUN mkdir ${HADOOP_HOME}/logs
RUN mkdir /hadoop-data

# Copy configuration files into the container
COPY ./conf ./conf
RUN mv ./conf/* ${HADOOP_CONF_DIR} 
RUN rm -rf ./conf

# Execute entrypoint file
COPY ./entrypoint.sh .

RUN chmod a+x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

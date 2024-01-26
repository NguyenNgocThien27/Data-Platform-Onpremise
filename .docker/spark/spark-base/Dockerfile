FROM hive-base:latest


# Defining useful environment variables
ENV SPARK_VERSION=3.2.1
ENV SCALA_VERSION=2.12.4
ENV SCALA_HOME=/usr/share/scala
ENV SPARK_HOME=/opt/spark
ENV SBT_HOME=/usr/local/sbt
ENV SBT_VERSION=1.4.9
ENV PYTHONHASHSEED=1
# ENV SPARK_EXECUTOR_MEMORY=650m
# ENV SPARK_DRIVER_MEMORY=650m
# ENV SPARK_WORKER_MEMORY=650m
# ENV SPARK_DAEMON_MEMORY=650m
ENV PATH $SPARK_HOME/bin/:$PATH

# Upgrade and install some tools and dependencies
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq \
    netcat \
    apt-utils \
    curl \
    vim \
    ssh \
    net-tools \
    ca-certificates \
    jq \
    wget \
    software-properties-common

# Installing Scala
WORKDIR /tmp

RUN wget --no-verbose "https://downloads.typesafe.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz" && \
    tar zxf scala-${SCALA_VERSION}.tgz && \
    mkdir ${SCALA_HOME} && \
    rm "scala-${SCALA_VERSION}/bin/"*.bat && \
    mv "scala-${SCALA_VERSION}/bin" "scala-${SCALA_VERSION}/lib" "${SCALA_HOME}" && \
    ln -s "${SCALA_HOME}/bin/*" "/usr/bin/" && \
    rm -rf *

# Installing SBT
RUN export PATH="${SBT_HOME}/bin:$PATH" && \ 
    apt-get update && \
    apt-get install ca-certificates wget tar && \
    mkdir -p "${SBT_HOME}" && \
    wget -qO - --no-check-certificate "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" | tar xz -C ${SBT_HOME} --strip-components=1 && \
    sbt sbtVersion

# Adding dependencies for PySpark
RUN apt-get install -y curl python3.9 python3.9-dev python3.9-distutils
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --set python /usr/bin/python3.9
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN pip install --upgrade pip
RUN apt-get install -yqq python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

#RUN apt-get install -yqq python3 python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy && \
#    update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1 && \
#    curl https://bootstrap.pypa.io/get-pip.py | python3

# Installing Spark
WORKDIR ${SPARK_HOME}
ENV TAIL_SPARK_TGZ_FILE=hadoop3.2
RUN wget --no-verbose https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-${TAIL_SPARK_TGZ_FILE}.tgz 
RUN tar zxf spark-${SPARK_VERSION}-bin-${TAIL_SPARK_TGZ_FILE}.tgz 
RUN mv spark-${SPARK_VERSION}-bin-${TAIL_SPARK_TGZ_FILE}/* . 
RUN rm -rf spark-${SPARK_VERSION}-bin-${TAIL_SPARK_TGZ_FILE}.tgz 
RUN rm -rf spark-${SPARK_VERSION}-bin-${TAIL_SPARK_TGZ_FILE}

# Use Spark with Hive
RUN cp ${HIVE_HOME}/conf/hive-site.xml $SPARK_HOME/conf

RUN apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/*

WORKDIR /

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
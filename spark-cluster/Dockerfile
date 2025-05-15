FROM python:3.12-bullseye AS spark-base

ARG SPARK_VERSION=3.5.5

# Install essential lib
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# ENV variables
ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

# Create home directory for hadoop and spark
RUN mkdir -p ${HADOOP_HOME}
RUN mkdir -p ${SPARK_HOME}

# Install spark, python
WORKDIR ${SPARK_HOME}
RUN curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-bin-hadoop3.tgz
# COPY ./spark-bin-hadoop3.tgz .
COPY ./requirements.txt .
COPY ./entrypoint.sh .
COPY ./submit.sh .

RUN tar -xvzf spark-bin-hadoop3.tgz --directory . --strip-components 1
RUN rm -rf spark-bin-hadoop3.tgz
RUN pip3 install -r requirements.txt
RUN chmod u+x ${SPARK_HOME}/sbin/*
RUN chmod u+x ${SPARK_HOME}/bin/*
RUN chmod u+x entrypoint.sh
RUN chmod u+x submit.sh

ENTRYPOINT ["./entrypoint.sh"]
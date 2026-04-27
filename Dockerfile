FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Installation Java 11 et utilitaires
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    curl \
    ssh \
    rsync \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Variables Hadoop
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Téléchargement et installation Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} $HADOOP_HOME \
    && rm hadoop-${HADOOP_VERSION}.tar.gz

# Copie des fichiers de configuration
COPY config/ $HADOOP_HOME/etc/hadoop/

# Configuration Java pour Hadoop
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Création des dossiers de données
RUN mkdir -p /opt/hadoop/data/namenode \
    && mkdir -p /opt/hadoop/data/datanode

# Configuration SSH
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 0600 ~/.ssh/authorized_keys

# Copie du script entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copie des scripts MapReduce
COPY mapreduce/ /mapreduce/

ENTRYPOINT ["/entrypoint.sh"]
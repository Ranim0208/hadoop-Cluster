#!/bin/bash

# Attendre que le namenode soit prêt
function wait_for_namenode() {
    echo "Waiting for namenode to be ready..."
    while ! hdfs dfs -ls / > /dev/null 2>&1; do
        sleep 2
    done
    echo "Namenode is ready!"
}

# Démarrer selon le rôle
case $NODE_TYPE in
    namenode)
        echo "Starting NameNode..."
        if [ ! -d /opt/hadoop/data/namenode/current ]; then
            echo "Formatting NameNode..."
            hdfs namenode -format -force -nonInteractive
        fi
        hdfs namenode &
        echo "Starting ResourceManager..."
        yarn resourcemanager
        ;;
    datanode)
        echo "Starting DataNode..."
        wait_for_namenode
        hdfs datanode &
        echo "Starting NodeManager..."
        yarn nodemanager
        ;;
    *)
        echo "ERROR: NODE_TYPE not set. Use 'namenode' or 'datanode'"
        exit 1
        ;;
esac
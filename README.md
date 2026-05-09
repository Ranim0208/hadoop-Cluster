# Hadoop + Spark Cluster sur Docker

Déploiement d'un cluster **Hadoop 3.3.6 + Spark 3.5.1** conteneurisé avec Docker, intégrant HDFS, YARN, MapReduce Streaming en Python et PySpark.

---

## Architecture

```
Docker Host
└── hadoop_network (bridge)
    ├── namenode      → NameNode + ResourceManager  (ports: 9870, 8088, 9000)
    ├── datanode1     → DataNode + NodeManager
    ├── datanode2     → DataNode + NodeManager
    ├── spark-master  → Spark Master               (ports: 8080, 7077)
    ├── spark-worker1 → Spark Worker
    └── spark-worker2 → Spark Worker
```

> Une **image Docker unique** est utilisée pour tous les nœuds.
> Le rôle de chaque container est déterminé par la variable d'environnement `NODE_TYPE`.

---

## Stack technique

| Technologie | Version |
|-------------|---------|
| Hadoop | 3.3.6 |
| Spark | 3.5.1 |
| Java | OpenJDK 11 |
| Python | 3.x |
| Ubuntu | 22.04 |
| Docker | latest |

---

## Structure du projet

```
hadoop-cluster/
├── Dockerfile                          ← Image unique (Hadoop + Spark + Python)
├── docker-compose.yml                  ← Orchestration des 6 services
├── .gitignore
├── config/
│   ├── core-site.xml                   ← Adresse du NameNode HDFS
│   ├── hdfs-site.xml                   ← Réplication HDFS = 2
│   ├── yarn-site.xml                   ← Hostname du ResourceManager
│   └── mapred-site.xml                 ← Framework MapReduce + variables env
├── scripts/
│   └── entrypoint.sh                   ← Démarrage selon NODE_TYPE
└── mapreduce/
    ├── analyse_CA_par_item/
    │   ├── mapper.py                   ← Extrait (item, prix)
    │   └── reducer.py                  ← Calcule CA total par item
    ├── analyse_meilleur_item/
    │   ├── mapper.py                   ← Extrait (item, prix)
    │   └── reducer.py                  ← Retourne l'item avec CA max
    ├── analyse_moyenne_store/
    │   ├── mapper.py                   ← Extrait (store, prix)
    │   └── reducer.py                  ← Calcule moyenne par store
    ├── analyse_item_par_store/
    │   ├── mapper.py                   ← Extrait (store, item)
    │   └── reducer.py                  ← Retourne l'item le plus vendu par store
    ├── data/
    │   ├── purchases.txt               ← Dataset principal (non versionné sur Git)
    │   ├── sessions.csv                ← Dataset jeux vidéo (généré)
    │   └── players.csv                 ← Profils joueurs (généré)
    └── spark/
        ├── generate_datasets.py        ← Génère sessions.csv et players.csv
        ├── spark_analysis.py           ← 3 KPIs PySpark
        └── verify_mapreduce.py         ← Vérification Spark SQL des résultats MapReduce
```

---

## Démarrage rapide

### Prérequis

- Docker Desktop installé et démarré
- Le fichier `purchases.txt` placé dans `mapreduce/data/`

### 1. Cloner le projet

```bash
git clone https://github.com/TON_USERNAME/hadoop-cluster-docker.git
cd hadoop-cluster-docker
```

### 2. Construire et démarrer le cluster

```bash
docker compose up --build -d
```

> ⏳ Le premier build prend environ 20-30 minutes (téléchargement de Hadoop + Spark).

### 3. Vérifier que les containers tournent

```bash
docker ps
```

Résultat attendu :

```
NAMES          STATUS
namenode       Up (healthy)
datanode1      Up
datanode2      Up
spark-master   Up
spark-worker1  Up
spark-worker2  Up
```

### 4. Vérifier le cluster HDFS

```bash
docker exec -it namenode bash
hdfs dfsadmin -report
# Résultat attendu : Live datanodes (2)
```

---

## Analyses MapReduce

### Chargement des données

```bash
docker exec -it namenode bash
hdfs dfs -mkdir -p /input
hdfs dfs -put /mapreduce/data/purchases.txt /input/
```

### Analyse 1 — Chiffre d'affaires par item

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files /mapreduce/analyse_CA_par_item/mapper.py,/mapreduce/analyse_CA_par_item/reducer.py \
    -input /input/purchases.txt \
    -output /output/chiffre_affaires \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Analyse 2 — Item le plus vendu selon le CA

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files /mapreduce/analyse_meilleur_item/mapper.py,/mapreduce/analyse_meilleur_item/reducer.py \
    -input /input/purchases.txt \
    -output /output/meilleur_item \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Analyse 3 — Moyenne de vente par store

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files /mapreduce/analyse_moyenne_store/mapper.py,/mapreduce/analyse_moyenne_store/reducer.py \
    -input /input/purchases.txt \
    -output /output/moyenne_store \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Analyse 4 — Item le plus vendu par store

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files /mapreduce/analyse_item_par_store/mapper.py,/mapreduce/analyse_item_par_store/reducer.py \
    -input /input/purchases.txt \
    -output /output/item_par_store \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Voir les résultats

```bash
hdfs dfs -cat /output/chiffre_affaires/part-00000
hdfs dfs -cat /output/meilleur_item/part-00000
hdfs dfs -cat /output/moyenne_store/part-00000
hdfs dfs -cat /output/item_par_store/part-00000
```

> ⚠️ Si un dossier de sortie existe déjà : `hdfs dfs -rm -r /output/nom_dossier`

---

## Partie Spark

### Générer les datasets

```bash
cd mapreduce/data
python3 ../spark/generate_datasets.py
```

### Charger dans HDFS

```bash
docker cp mapreduce/data/sessions.csv namenode:/tmp/sessions.csv
docker cp mapreduce/data/players.csv namenode:/tmp/players.csv

docker exec -it namenode bash
hdfs dfs -mkdir -p /data
hdfs dfs -put /tmp/sessions.csv /data/
hdfs dfs -put /tmp/players.csv /data/
```

### Lancer l'analyse Spark (3 KPIs)

```bash
docker cp mapreduce/spark/spark_analysis.py spark-master:/tmp/spark_analysis.py

docker exec -it spark-master bash
spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /tmp/spark_analysis.py
```

### Vérification Spark SQL

```bash
docker cp mapreduce/spark/verify_mapreduce.py spark-master:/tmp/verify_mapreduce.py

docker exec -it spark-master bash
spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /tmp/verify_mapreduce.py
```

---

## 🛑 Arrêter le cluster

```bash
docker compose down
```

> Les données HDFS sont conservées dans les volumes Docker.

---

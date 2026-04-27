# 🐘 Hadoop Cluster sur Docker

Déploiement d'un cluster **Hadoop 3.3.6** conteneurisé avec Docker, intégrant HDFS, YARN et MapReduce Streaming en Python.

---

## 🏗️ Architecture

```
hadoop-cluster/
├── Dockerfile                  ← Image unique (namenode + datanode)
├── docker-compose.yml          ← Orchestration du cluster
├── config/
│   ├── core-site.xml           ← Configuration HDFS
│   ├── hdfs-site.xml           ← Réplication & stockage
│   ├── yarn-site.xml           ← Gestionnaire de ressources
│   └── mapred-site.xml         ← Framework MapReduce
├── scripts/
│   └── entrypoint.sh           ← Démarrage intelligent selon NODE_TYPE
└── mapreduce/
    ├── mapper.py               ← Extraction item + prix
    └── reducer.py              ← Agrégation du chiffre d'affaires
```

### Topologie du cluster

```
Docker Host
└── hadoop_network (bridge)
    ├── namenode   → NameNode + ResourceManager  (ports: 9870, 8088, 9000)
    ├── datanode1  → DataNode + NodeManager
    └── datanode2  → DataNode + NodeManager
```

> Une **image Docker unique** est utilisée pour tous les nœuds.
> Le rôle de chaque conteneur est déterminé par la variable d'environnement `NODE_TYPE`.

---

## ⚙️ Stack technique

| Technologie | Version |
|-------------|---------|
| Hadoop | 3.3.6 |
| Java | OpenJDK 11 |
| Python | 3.x |
| Ubuntu | 22.04 |
| Docker | latest |

---

## 🚀 Démarrage rapide

### Prérequis

- Docker Desktop installé et démarré
- Git installé
- Le fichier `purchases.txt` fourni par l'enseignant placé dans `mapreduce/`

### 1. Cloner le projet

```bash
git clone https://github.com/TON_USERNAME/hadoop-cluster-docker.git
cd hadoop-cluster-docker
```

### 2. Construire et démarrer le cluster

```bash
docker compose up --build -d
```

> ⏳ Le premier build prend environ 10-20 minutes (téléchargement de Hadoop).

### 3. Vérifier que les conteneurs tournent

```bash
docker ps
```

Résultat attendu :

```
NAMES       STATUS
namenode    Up (healthy)
datanode1   Up
datanode2   Up
```

---

## 📊 Exécution du job MapReduce

### 1. Charger les données dans HDFS

```bash
hdfs dfs -mkdir -p /input
hdfs dfs -put /mapreduce/purchases.txt /input/
hdfs dfs -ls /input/
```

### 2. Tester les scripts localement

```bash
head -5 /mapreduce/purchases.txt | python3 /mapreduce/mapper.py
```

Résultat attendu :

```
Men's Clothing    214.05
Women's Clothing  153.57
Music             66.08
```

Pipeline complet :

```bash
cat /mapreduce/purchases.txt | python3 /mapreduce/mapper.py | sort | python3 /mapreduce/reducer.py | head -5
```

### 3. Lancer le job

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /input/purchases.txt \
    -output /output/chiffre_affaires \
    -mapper "python3 /mapreduce/mapper.py" \
    -reducer "python3 /mapreduce/reducer.py"
```

### 4. Afficher les résultats

```bash
hdfs dfs -cat /output/chiffre_affaires/part-00000
```

Résultats attendus :

```
Baby                    57491808.44
Books                   57450757.91
CDs                     57410753.04
Cameras                 57299046.64
Children's Clothing     57624820.94
Computers               57315406.32
Consumer Electronics    57452374.13
DVDs                    57649212.14
...
```

---

## 🔁 Relancer un job

Hadoop refuse d'écrire dans un dossier de sortie existant. Supprimer d'abord l'ancien output :

```bash
hdfs dfs -rm -r /output/chiffre_affaires
```

---

## 🛑 Arrêter le cluster

```bash
docker compose down
```

> ⚠️ Les données HDFS sont perdues à l'arrêt car stockées dans les conteneurs.
> Pour les persister, les volumes Docker sont déjà configurés dans le `docker-compose.yml`.

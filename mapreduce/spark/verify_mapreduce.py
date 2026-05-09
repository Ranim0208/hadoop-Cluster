from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, round, col, max

spark = SparkSession.builder \
    .appName("VerificationMapReduce") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Lire purchases.txt depuis HDFS
df = spark.read.csv("hdfs://namenode:9000/input/purchases.txt",
                     sep="\t", inferSchema=True)
df = df.toDF("date", "time", "store", "item", "cost", "payment")

# ── Vérification 1 : Chiffre d'affaires par store ─────────────────────────────
print("\n===== Vérification 1 : Chiffre d'affaires par store =====")
df.groupBy("store") \
  .agg(round(sum("cost"), 2).alias("chiffre_affaires")) \
  .orderBy("store") \
  .show()

# ── Vérification 2 : Item le plus vendu (CA) ──────────────────────────────────
print("\n===== Vérification 2 : Item le plus vendu selon CA =====")
df.groupBy("item") \
  .agg(round(sum("cost"), 2).alias("chiffre_affaires")) \
  .orderBy(col("chiffre_affaires").desc()) \
  .limit(1) \
  .show()

# ── Vérification 3 : Moyenne de vente par store ───────────────────────────────
print("\n===== Vérification 3 : Moyenne de vente par store =====")
df.groupBy("store") \
  .agg(round(avg("cost"), 2).alias("moyenne_vente")) \
  .orderBy("store") \
  .show()

# ── Vérification 4 : Item le plus vendu par store ─────────────────────────────
print("\n===== Vérification 4 : Item le plus vendu par store =====")
df.groupBy("store", "item") \
  .agg(count("item").alias("nb_ventes")) \
  .groupBy("store") \
  .agg(max(col("nb_ventes")).alias("max_ventes")) \
  .orderBy("store") \
  .show()

spark.stop()
print("\nVerification terminee !")
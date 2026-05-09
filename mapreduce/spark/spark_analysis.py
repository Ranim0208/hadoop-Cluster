import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, round, col

# ─── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # ─── SESSION SPARK ────────────────────────────────────────────────────────
    spark = SparkSession.builder \
        .appName("GameAnalytics") \
        .master("spark://spark-master:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    logger.info("Spark session started successfully")

    # ─── LECTURE DES DONNÉES ──────────────────────────────────────────────────
    logger.info("Reading datasets from HDFS...")
    sessions = spark.read.csv("hdfs://namenode:9000/data/sessions.csv",
                               header=True, inferSchema=True)
    players = spark.read.csv("hdfs://namenode:9000/data/players.csv",
                              header=True, inferSchema=True)

    logger.info(f"Sessions dataset: {sessions.count()} rows")
    logger.info(f"Players dataset: {players.count()} rows")

    # ─── JOINTURE ─────────────────────────────────────────────────────────────
    df = sessions.join(players, on="player_id", how="left")
    logger.info("Join between sessions and players completed")

    # ─── KPI 1 : Statistiques par joueur ──────────────────────────────────────
    logger.info("Computing KPI 1: Player statistics...")
    player_stats = df.groupBy("player_id", "username").agg(
        round(avg("duration_min"), 2).alias("avg_session_duration"),
        round(avg("xp_earned"), 2).alias("avg_xp_earned"),
        round(avg("quests_completed"), 2).alias("avg_quests_completed")
    )
    player_stats.write.mode("overwrite").parquet("hdfs://namenode:9000/output/player_stats")
    logger.info("KPI 1 saved to HDFS: /output/player_stats")

    # ─── KPI 2 : Métriques par genre ──────────────────────────────────────────
    logger.info("Computing KPI 2: Metrics by genre...")
    genre_metrics = df.groupBy("genre").agg(
        round(avg("quests_completed"), 2).alias("avg_quests_per_genre"),
        round(avg("duration_min"), 2).alias("avg_session_duration"),
        round(avg("total_hours"), 2).alias("avg_total_hours")
    )
    genre_metrics.write.mode("overwrite").parquet("hdfs://namenode:9000/output/genre_metrics")
    logger.info("KPI 2 saved to HDFS: /output/genre_metrics")

    # ─── KPI 3 : Métriques par niveau de joueur ───────────────────────────────
    logger.info("Computing KPI 3: Metrics by player level...")
    level_metrics = df.groupBy("player_level").agg(
        round(avg("enemies_killed"), 2).alias("avg_enemies_killed")
    )
    level_metrics.write.mode("overwrite").parquet("hdfs://namenode:9000/output/level_metrics")
    logger.info("KPI 3 saved to HDFS: /output/level_metrics")

    # ─── VERIFICATION SPARK SQL ───────────────────────────────────────────────
    logger.info("Verifying results with Spark SQL...")

    spark.read.parquet("hdfs://namenode:9000/output/player_stats").createOrReplaceTempView("player_stats")
    spark.read.parquet("hdfs://namenode:9000/output/genre_metrics").createOrReplaceTempView("genre_metrics")
    spark.read.parquet("hdfs://namenode:9000/output/level_metrics").createOrReplaceTempView("level_metrics")

    print("\n===== KPI 1 : Statistiques par joueur (top 5) =====")
    spark.sql("SELECT * FROM player_stats LIMIT 5").show()

    print("\n===== KPI 2 : Métriques par genre =====")
    spark.sql("SELECT * FROM genre_metrics ORDER BY genre").show()

    print("\n===== KPI 3 : Ennemis éliminés par niveau =====")
    spark.sql("SELECT * FROM level_metrics ORDER BY player_level").show()

    logger.info("All KPIs computed and saved successfully!")
    spark.stop()

if __name__ == "__main__":
    main()
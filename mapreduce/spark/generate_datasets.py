import csv
import random

genres = ["RPG", "FPS", "Strategy", "Sports", "Adventure"]
levels = ["Beginner", "Intermediate", "Advanced", "Expert"]

# Dataset 1 : sessions de jeu
with open("sessions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["session_id", "player_id", "genre", "duration_min",
                     "xp_earned", "quests_completed", "enemies_killed", "player_level"])
    for i in range(1, 10001):
        writer.writerow([
            i,
            random.randint(1, 1000),
            random.choice(genres),
            random.randint(10, 300),
            random.randint(50, 5000),
            random.randint(0, 20),
            random.randint(0, 200),
            random.choice(levels)
        ])

# Dataset 2 : profils joueurs
with open("players.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["player_id", "username", "age", "country", "total_hours"])
    for i in range(1, 1001):
        writer.writerow([
            i,
            f"player_{i}",
            random.randint(12, 50),
            random.choice(["France", "USA", "Germany", "Japan", "Brazil"]),
            random.randint(1, 2000)
        ])

print("datasets generated: sessions.csv, players.csv")
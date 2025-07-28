import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='H@rish052005',
    database='spotify_db'
)

# Query for popularity range distribution
query = """
SELECT 
    CASE 
        WHEN popularity >= 80 THEN 'Very Popular'
        WHEN popularity >= 50 THEN 'Popular'
        ELSE 'Less Popular'
    END AS popularity_range,
    COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY popularity_range;
"""

df = pd.read_sql(query, conn)
conn.close()

# Plot
colors = ['green', 'orange', 'red']
df.plot(kind='bar', x='popularity_range', y='track_count', color=colors, legend=False, edgecolor='black')

plt.title("Spotify Track Popularity Distribution")
plt.xlabel("Popularity Category")
plt.ylabel("Number of Tracks")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

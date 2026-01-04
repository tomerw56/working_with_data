import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="demo",
    password="demo",
    dbname="demo"
)

cur = conn.cursor()

# Enable PostGIS
cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

# --- JSON demo ---
cur.execute("""
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    profile JSONB
);
""")

users = [
    ("Alice", {"age": 30, "skills": ["python", "sql"], "active": True}),
    ("Bob",   {"age": 42, "skills": ["java"], "active": False}),
    ("Carol", {"age": 27, "skills": ["python", "geo"], "active": True})
]

for name, profile in users:
    cur.execute(
        "INSERT INTO users (name, profile) VALUES (%s, %s)",
        (name, json.dumps(profile))
    )

# --- Array demo ---
cur.execute("""
DROP TABLE IF EXISTS projects;
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT,
    tags TEXT[]
);
""")

cur.execute("""
INSERT INTO projects (name, tags) VALUES
('Search', ARRAY['backend', 'elasticsearch']),
('Maps', ARRAY['geo', 'frontend']),
('Analytics', ARRAY['python', 'data']);
""")

# --- Geo demo ---
cur.execute("""
DROP TABLE IF EXISTS stores;
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name TEXT,
    location GEOGRAPHY(Point, 4326)
);
""")

cur.execute("""
INSERT INTO stores (name, location) VALUES
('Tel Aviv Store', ST_MakePoint(34.7818, 32.0853)),
('Jerusalem Store', ST_MakePoint(35.2137, 31.7683));
""")

conn.commit()
cur.close()
conn.close()

print("✅ Database loaded with JSON, arrays, and geospatial data")

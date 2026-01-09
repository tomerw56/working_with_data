
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="demo",
    password="demo",
    dbname="demo"
)
cur = conn.cursor()

cur.execute("""
INSERT INTO users (name, profile)
SELECT name, profile FROM users
CROSS JOIN generate_series(1, 5000);
""")


import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="demo",
    password="demo",
    dbname="demo"
)
cur = conn.cursor()

cur.execute("""
SELECT name
FROM users
WHERE profile->>'active' = 'true'
  AND profile->'skills' ? 'python'
""")

print(cur.fetchall())

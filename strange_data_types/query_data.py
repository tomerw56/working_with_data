import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="demo",
    password="demo",
    dbname="demo"
)

cur = conn.cursor()

print("\n🟢 Active users (JSON):")
cur.execute("""
SELECT name
FROM users
WHERE profile->>'active' = 'true';
""")
print(cur.fetchall())

print("\n🟢 Projects with 'geo' tag (ARRAY):")
cur.execute("""
SELECT name
FROM projects
WHERE 'geo' = ANY(tags);
""")
print(cur.fetchall())

print("\n🟢 Users near Tel Aviv store (JSON + GEO):")
cur.execute("""
SELECT u.name, s.name
FROM users u
JOIN stores s
  ON ST_DWithin(
       s.location,
       ST_MakePoint(34.78, 32.08),
       50000
     )
WHERE u.profile->>'active' = 'true'
  AND u.profile->'skills' ? 'python';
""")
print(cur.fetchall())

cur.close()
conn.close()

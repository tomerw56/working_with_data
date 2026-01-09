import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

# --- Raw SQL ---
conn = psycopg2.connect(
    host="localhost",
    user="demo",
    password="demo",
    dbname="demo"
)
cur = conn.cursor()

start = time.perf_counter()
cur.execute("""
SELECT name
FROM users
WHERE profile->>'active' = 'true'
  AND profile->'skills' ? 'python'
""")
raw_result = cur.fetchall()
raw_time = time.perf_counter() - start

# --- ORM ---
engine = create_engine("postgresql://demo:demo@localhost:5432/demo")
Session = sessionmaker(bind=engine)
session = Session()

start = time.perf_counter()
orm_result = (
    session.query(User)
    .filter(User.profile["active"].astext == "true")
    .filter(User.profile["skills"].contains(["python"]))
    .all()
)
orm_time = time.perf_counter() - start

print(f"Raw SQL: {raw_time:.4f}s ({len(raw_result)} rows)")
print(f"ORM     : {orm_time:.4f}s ({len(orm_result)} rows)")

import psycopg2

conn=psycopg2.connect(
    host="127.0.0.1",
    user="postgres",
    dbname="postgres",
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer TEXT,
    amount INT
)
""")

cur.execute("INSERT INTO orders (customer, amount) VALUES (%s, %s)",
            ("Alice", 120))

cur.execute("""
SELECT customer, SUM(amount)
FROM orders
GROUP BY customer
""")

print(cur.fetchall())

conn.commit()
conn.close()

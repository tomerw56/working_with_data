import duckdb

con = duckdb.connect()

con.execute("""
INSTALL httpfs;
LOAD httpfs;

SET s3_endpoint='localhost:9000';
SET s3_access_key_id='minio';
SET s3_secret_access_key='minio123';
SET s3_use_ssl=false;
SET s3_url_style='path';
""")

print("📊 CSV aggregation:")
print(con.execute("""
SELECT country, COUNT(*) AS cnt, AVG(value) AS avg_value
FROM read_csv_auto('s3://lake/csv/events.csv')
GROUP BY country
""").fetchdf())

print("\n📊 JSON events:")
print(con.execute("""
SELECT event, COUNT(*)
FROM read_json_auto('s3://lake/json/events.json')
GROUP BY event
""").fetchdf())

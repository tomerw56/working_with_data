import duckdb
import time

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

QUERY = """
SELECT country, AVG(value)
FROM {source}
GROUP BY country
"""

def timed_query(label, source):
    start = time.perf_counter()
    df = con.execute(QUERY.format(source=source)).fetchdf()
    duration = time.perf_counter() - start
    print(f"\n{label}")
    print(df)
    print(f"⏱️ Time: {duration:.6f} seconds")

# Raw CSV (schema-on-read, parsing every time)
timed_query(
    "Raw lake (CSV)",
    "read_csv_auto('s3://lake/csv/events.csv')"
)

# Schema lake (Parquet, typed, columnar)
timed_query(
    "Schema lake (Parquet)",
    "'s3://schemalake/parquet/events.parquet'"
)

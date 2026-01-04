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

# Build Level-1 (schema applied) lake
con.execute("""
COPY (
    SELECT
        CAST(user_id AS INTEGER) AS user_id,
        country,
        CAST(value AS INTEGER) AS value,
        CAST(ts AS TIMESTAMP) AS ts
    FROM read_csv_auto('s3://lake/csv/events.csv')
)
TO 's3://schemalake/parquet/events.parquet'
(FORMAT PARQUET);
""")

print("✅ Schema lake built (Parquet with types)")

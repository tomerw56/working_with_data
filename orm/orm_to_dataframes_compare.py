import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from models import User
import pandas as pd
import polars as pl

DB_URL = "postgresql://demo:demo@localhost:5432/demo"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

session = Session()
print ("ORM")
start = time.perf_counter()

users = (
    session.query(User.name)
    .filter(User.profile["active"].astext == "true")
    .filter(User.profile["skills"].has_key("python"))
    .all()
)

orm_time = time.perf_counter() - start
session.close()
print(f"ORM    : {orm_time:.4f}s")

print("PANDAS")
start = time.perf_counter()

df = pd.read_sql("SELECT * FROM users", engine)

result = df[
    (df["profile"].apply(lambda p: p["active"])) &
    (df["profile"].apply(lambda p: "python" in p["skills"]))
]

pandas_time = time.perf_counter() - start
print(f"Pandas : {pandas_time:.4f}s")

print("POLARS")
start = time.perf_counter()

df = pl.read_database_uri(
    "SELECT * FROM users",
    DB_URL
)

# Decode JSON string into struct
df = df.with_columns(
    pl.col("profile").str.json_decode(
        dtype=pl.Struct([
            pl.Field("active", pl.Boolean),
            pl.Field("skills", pl.List(pl.Utf8))
        ])
    ).alias("profile")
)

# Now you can filter
result = (
    df
    .filter(pl.col("profile").struct.field("active") == True)
    .filter(
        pl.col("profile")
        .struct.field("skills")
        .list.contains("python")
    )
    .select("name")
)


polars_time = time.perf_counter() - start



print(f"Polars : {polars_time:.4f}s")

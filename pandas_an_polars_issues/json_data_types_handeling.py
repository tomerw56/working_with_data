"""
Pandas vs Polars – Complex Data Types & Performance Demo (Fixed)

Focus:
- Avoiding row-wise iteration
- JSON / nested data handling
- List fields
- Lazy execution & optimization

Requirements:
  pip install pandas polars numpy
"""

import time
import json
import numpy as np
import pandas as pd
import polars as pl

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
N = 1_000_000
COUNTRIES = ["IL", "US", "DE"]

# Explicit Polars schema for JSON decoding
PAYLOAD_DTYPE = pl.Struct({
    "user": pl.Struct({
        "id": pl.Int64,
        "country": pl.Utf8,
    }),
    "metrics": pl.Struct({
        "cpu": pl.Float64,
        "mem": pl.Int64,
    }),
    "tags": pl.List(pl.Utf8),
})


def generate_payloads(n: int):
    """Generate JSON payloads with nested + list data."""
    return [
        json.dumps({
            "user": {
                "id": i,
                "country": np.random.choice(COUNTRIES)
            },
            "metrics": {
                "cpu": np.random.random(),
                "mem": np.random.randint(100, 1000)
            },
            "tags": ["prod", "api"] if i % 2 == 0 else ["prod"]
        })
        for i in range(n)
    ]


# ------------------------------------------------------------
# Pandas – JSON + apply (Anti-pattern)
# ------------------------------------------------------------
def pandas_json_apply(payloads):
    print("\n=== Pandas: JSON + apply (slow) ===")

    df = pd.DataFrame({"payload": payloads})

    start = time.time()

    df["country"] = df["payload"].apply(
        lambda x: json.loads(x)["user"]["country"]
    )
    df["cpu"] = df["payload"].apply(
        lambda x: json.loads(x)["metrics"]["cpu"]
    )

    result = (
        df[df["cpu"] > 0.7]
        .groupby("country")
        .size()
    )

    elapsed = time.time() - start
    print(f"Pandas time: {elapsed:.2f}s")
    print(result)


# ------------------------------------------------------------
# Polars – Eager, Vectorized JSON
# ------------------------------------------------------------
def polars_json_eager(payloads):
    print("\n=== Polars: Eager JSON decode ===")

    df = pl.DataFrame({"payload": payloads})

    start = time.time()

    result = (
        df.with_columns(
            pl.col("payload")
              .str.json_decode(dtype=PAYLOAD_DTYPE)
              .alias("payload")
        )
        .with_columns(
            country=pl.col("payload")
                .struct.field("user")
                .struct.field("country"),
            cpu=pl.col("payload")
                .struct.field("metrics")
                .struct.field("cpu"),
        )
        .filter(pl.col("cpu") > 0.7)
        .group_by("country")
        .count()
    )

    elapsed = time.time() - start
    print(f"Polars eager time: {elapsed:.2f}s")
    print(result)


# ------------------------------------------------------------
# Polars – Lazy + Optimizer
# ------------------------------------------------------------
def polars_json_lazy(payloads):
    print("\n=== Polars: Lazy + optimized ===")

    df = pl.DataFrame({"payload": payloads})

    start = time.time()

    result = (
        df.lazy()
        .with_columns(
            pl.col("payload")
              .str.json_decode(dtype=PAYLOAD_DTYPE)
              .alias("payload")
        )
        .with_columns(
            country=pl.col("payload")
                .struct.field("user")
                .struct.field("country"),
            cpu=pl.col("payload")
                .struct.field("metrics")
                .struct.field("cpu"),
        )
        .filter(pl.col("cpu") > 0.7)   # predicate pushdown
        .group_by("country")
        .count()
        .collect()
    )

    elapsed = time.time() - start
    print(f"Polars lazy time: {elapsed:.2f}s")
    print(result)


# ------------------------------------------------------------
# Polars – List Field Query (no explode)
# ------------------------------------------------------------
def polars_list_query(payloads):
    print("\n=== Polars: List field filtering ===")

    df = pl.DataFrame({"payload": payloads})

    start = time.time()

    result = (
        df.lazy()
        .with_columns(
            pl.col("payload")
              .str.json_decode(dtype=PAYLOAD_DTYPE)
              .alias("payload")
        )
        .filter(
            pl.col("payload")
              .struct.field("tags")
              .list.contains("api")  # <- updated line
        )
        .count()
        .collect()
    )

    elapsed = time.time() - start
    print(f"Polars list-any time: {elapsed:.2f}s")
    print(result)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    print(f"Generating {N:,} JSON payloads...")
    payloads = generate_payloads(N)

    pandas_json_apply(payloads)
    polars_json_eager(payloads)
    polars_json_lazy(payloads)
    polars_list_query(payloads)

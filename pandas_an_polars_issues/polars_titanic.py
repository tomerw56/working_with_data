
"""
Polars Titanic Parquet Demo

Requires:
    pip install polars
    download data from https://github.com/aws-samples/acclerate-research-with-real-world-data-using-aws-data-exchange-for-amazon-redshift/blob/main/titanic.parquet
"""

import polars as pl
import time

# Replace this with your local path if needed
PARQUET_FILE = "titanic.parquet"

def eager_scan_and_summary():
    print("\n=== Polars eager scan + summary ===")
    start = time.time()

    df = pl.read_parquet(PARQUET_FILE)

    # Basic summary
    summary = (
        df.group_by("Survived")
        .agg([
            pl.count(),                 # number of rows per survival
            pl.col("Age").mean().alias("avg_age"),
            pl.col("Fare").mean().alias("avg_fare"),
        ])
    )

    print("Time (eager):", time.time() - start)
    print(summary)


def lazy_filter_and_select():
    print("\n=== Polars lazy scan + filter & projection ===")
    start = time.time()

    result = (
        pl.scan_parquet(PARQUET_FILE)      # lazy parquet scan
        .filter(pl.col("Age") > 30)        # filter pushdown
        .select([
            "Survived",
            "Sex",
            "Age",
            "Fare",
        ])
        .collect()
    )

    print("Time (lazy):", time.time() - start)
    print(result.head(10))


def groupby_survival_stats():
    print("\n=== Polars lazy groupby + aggregation ===")
    start = time.time()

    result = (
        pl.scan_parquet(PARQUET_FILE)      # lazy parquet scan
        .group_by("Survived")
        .agg([
            pl.col("Fare").mean().alias("avg_fare"),
            pl.col("Age").median().alias("median_age"),
        ])
        .collect()
    )

    print("Time (lazy groupby):", time.time() - start)
    print(result)


if __name__ == "__main__":
    eager_scan_and_summary()
    lazy_filter_and_select()
    groupby_survival_stats()

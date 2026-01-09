import polars as pl
import numpy as np
import time

N = 50_000_000


df = pl.DataFrame({
    "a": np.random.randint(0, 100, N),
    "b": np.random.randint(0, 100, N),
})

start = time.time()

df = df.with_columns(
    (pl.col("a") * 2 + pl.col("b")).alias("c")
)

print("Polars eager time:", time.time() - start)

start = time.time()

df = (
    df.lazy()
      .with_columns((pl.col("a") * 2 + pl.col("b")).alias("c"))
      .select(["c"])  # projection pruning
      .collect()
)

print("Polars lazy optimized time:", time.time() - start)

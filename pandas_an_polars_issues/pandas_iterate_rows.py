import pandas as pd
import numpy as np
import time

N = 5_000_000

df = pd.DataFrame({
    "a": np.random.randint(0, 100, N),
    "b": np.random.randint(0, 100, N),
})

start = time.time()

result = []
for _, row in df.iterrows():
    result.append(row["a"] * 2 + row["b"])

df["c"] = result

print("Pandas iterrows time:", time.time() - start)

start = time.time()

df["c"] = df["a"] * 2 + df["b"]

print("Pandas vectorized time:", time.time() - start)

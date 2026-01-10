"""
Titanic Survival Analysis:
Statistics vs LLM Reasoning

Requirements:
  pip install polars scipy matplotlib
  ollama running locally (ollama run llama3)

Dataset:
  titanic.parquet (from AWS samples repo)
"""

import json
import subprocess

import polars as pl
from scipy.stats import chi2_contingency, mannwhitneyu


# ------------------------------------------------------------
# Load & clean data
# ------------------------------------------------------------

df = pl.scan_parquet("titanic.parquet")

df_clean = (
    df.with_columns(
        pl.col("Age").fill_null(pl.col("Age").median()),
        pl.col("Fare").fill_null(pl.col("Fare").median()),
        pl.col("Embarked").fill_null("S"),
    )
)

# ------------------------------------------------------------
# Survival rates (interpretable insight)
# ------------------------------------------------------------

survival_by_class = (
    df_clean
    .group_by("Pclass")
    .agg(pl.col("Survived").mean().alias("survival_rate"))
    .sort("Pclass")
    .collect()
)

survival_by_sex = (
    df_clean
    .group_by("Sex")
    .agg(pl.col("Survived").mean().alias("survival_rate"))
    .collect()
)

df_age = df_clean.with_columns(
    pl.when(pl.col("Age") < 12).then(pl.lit("Child"))
    .when(pl.col("Age") < 60).then(pl.lit("Adult"))
    .otherwise(pl.lit("Senior"))
    .alias("age_group")
)

survival_by_age = (
    df_age
    .group_by("age_group")
    .agg(pl.col("Survived").mean().alias("survival_rate"))
    .collect()
)
# ------------------------------------------------------------
# Statistical tests
# ------------------------------------------------------------

# --- Class vs Survival (Chi-square) ---
class_counts = (
    df_clean
    .group_by("Pclass")
    .agg([
        (pl.col("Survived") == 1).sum().alias("survived"),
        (pl.col("Survived") == 0).sum().alias("died"),
    ])
    .collect()
)

chi2_class, p_class, _, _ = chi2_contingency(
    class_counts.select(["survived", "died"]).to_numpy()
)

# --- Age vs Survival (Mann–Whitney U) ---
ages_survived = (
    df_clean.filter(pl.col("Survived") == 1)
    .select("Age")
    .collect()
    .to_numpy()
    .ravel()
)

ages_died = (
    df_clean.filter(pl.col("Survived") == 0)
    .select("Age")
    .collect()
    .to_numpy()
    .ravel()
)

u_stat, p_age = mannwhitneyu(ages_survived, ages_died)

print("llm data preperation")
# ------------------------------------------------------------
# Prepare data for LLM
# ------------------------------------------------------------

llm_input = {
    "survival_by_class": {
        str(row["Pclass"]): round(row["survival_rate"], 3)
        for row in survival_by_class.to_dicts()
    },
    "survival_by_age_group": {
        row["age_group"]: round(row["survival_rate"], 3)
        for row in survival_by_age.to_dicts()
    },
    "statistics": {
        "class_chi_square_p_value": p_class,
        "age_mann_whitney_p_value": p_age,
    }
}

prompt = f"""
You are analyzing Titanic survival data.

Aggregated evidence:
{json.dumps(llm_input, indent=2)}

Question:
Which factor had a bigger importance for surviving the Titanic:
age or passenger class?

Rules:
- Base your answer ONLY on the data above
- Compare effect size, not just significance
- Give a clear conclusion
"""

print (f"prompt :: {prompt}")

# ------------------------------------------------------------
# Call Ollama
# ------------------------------------------------------------

result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=prompt,
    text=True,
    capture_output=True
)

print("\n=== STATISTICAL CONCLUSION ===")
print(f"Passenger class p-value: {p_class:.3e}")
print(f"Age p-value:             {p_age:.3e}")
print("Conclusion: Passenger class has a stronger effect than age.")

print("\n=== LLM CONCLUSION ===")
print(result.stdout)

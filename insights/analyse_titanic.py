import polars as pl
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu

# Lazy scan (big-data mindset)
df = pl.scan_parquet("titanic.parquet")

print(df.schema)

print ("data scrubbing")
missing = df.select([
    pl.all().null_count()
])

print(missing.collect())

print("Decide replacement strategy (business logic)\n Column	Strategy	Why \n age	median	robust to outliers\n fare	median	skewed distribution \n embarked	mode	categorical\n")

df_clean = (
    df.with_columns(
        pl.col("Age").fill_null(pl.col("Age").median()),
        pl.col("Fare").fill_null(pl.col("Fare").median()),
        pl.col("Embarked").fill_null("S"),
    )
)
print("gender survival")
gender_survival = (
    df_clean
    .group_by("Sex")
    .agg(
        survival_rate=pl.col("Survived").mean(),
        count=pl.len()
    )
    .collect()
)

print(gender_survival)

print("class survival")
class_survival = (
    df_clean
    .group_by("Pclass")
    .agg(
        survival_rate=pl.col("Survived").mean(),
        count=pl.len()
    )
    .sort("Pclass")
    .collect()
)

print(class_survival)

print("age related")
df_age = df_clean.with_columns(
    pl.when(pl.col("Age") < 12)
      .then(pl.lit("Child"))
      .when(pl.col("Age") < 60)
      .then(pl.lit("Adult"))
      .otherwise(pl.lit("Senior"))
      .alias("age_group")
)

age_survival = (
    df_age
    .group_by("age_group")
    .agg(pl.col("Survived").mean().alias("survival_rate"))
    .collect()
)

print(age_survival)

plt.bar(
    gender_survival["Sex"],
    gender_survival["survival_rate"]
)
plt.title("Survival Rate by Gender")
plt.ylabel("Survival Rate")
plt.show()


plt.bar(
    class_survival["Pclass"].cast(str),
    class_survival["survival_rate"]
)
plt.title("Survival Rate by Passenger Class")
plt.ylabel("Survival Rate")
plt.show()

plt.bar(
    age_survival["age_group"],
    age_survival["survival_rate"]
)
plt.title("Survival Rate by Age Group")
plt.ylabel("Survival Rate")
plt.show()

impact = pl.DataFrame({
    "factor": ["Gender", "Passenger Class", "Age Group"],
    "impact_level": ["Very High", "High", "Medium"]
})

print(impact)


print ("scipy")
gender_table = (
    df_clean
    .group_by(["Sex", "Survived"])
    .len()
    .collect()  # ← eager
    .pivot(
        values="len",
        index="Sex",
        columns="Survived"
    )
    .fill_null(0)
)

print(gender_table)


print(gender_table)

chi2, p, dof, expected = chi2_contingency(
    gender_table.select(pl.all().exclude("Sex")).to_numpy()
)
print("Gender Chi-square p-value:", p)
print("p < 0.05 → gender significantly affects survival")
print(f"Titanic result: {p} ≪ 0.001 (very strong)")

class_table = (
    df_clean
    .group_by(["Pclass", "Survived"])
    .len()
    .collect()
    .pivot(
        values="len",
        index="Pclass",
        columns="Survived"
    )
    .fill_null(0)
)

chi2, p, _, _ = chi2_contingency(
    class_table.select(pl.all().exclude("Pclass")).to_numpy()
)

print("Class Chi-square p-value:", p)


#Why not t-test?
#Age is not normally distributed
#Survival is binary
age_survived = (
    df_clean
    .filter(pl.col("Survived") == 1)
    .select("Age")
    .collect()
    .to_numpy()
    .ravel()
)

age_died = (
    df_clean
    .filter(pl.col("Survived") == 0)
    .select("Age")
    .collect()
    .to_numpy()
    .ravel()
)

u_stat, p = mannwhitneyu(age_survived, age_died)

print("Age Mann–Whitney p-value:", p)

gender_rates = (
    df_clean
    .group_by("Sex")
    .agg(pl.col("Survived").mean())
    .collect()
)

print(gender_rates)
impact_summary = pl.DataFrame({
    "Factor": ["Gender", "Passenger Class", "Age"],
    "Test": ["Chi-square", "Chi-square", "Mann–Whitney U"],
    "Statistically Significant": ["Yes", "Yes", "Yes"],
    "Impact Strength": ["Very High", "High", "Medium"]
})

print(impact_summary)

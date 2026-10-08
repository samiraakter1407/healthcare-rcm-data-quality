import pandas as pd

# Load raw dataset
df = pd.read_csv("data/raw/healthcare_dataset.csv")

print("=== DATA QUALITY CHECKS ===")

# 1. Duplicate records
duplicate_count = df.duplicated().sum()
print(f"\nDuplicate rows: {duplicate_count}")

# 2. Missing values
missing_values = df.isnull().sum().sum()
print(f"Missing values: {missing_values}")

# 3. Invalid ages
invalid_age_count = ((df["Age"] < 0) | (df["Age"] > 120)).sum()
print(f"Invalid ages: {invalid_age_count}")

# 4. Negative billing amounts
negative_billing_count = (df["Billing Amount"] < 0).sum()
print(f"Negative billing amounts: {negative_billing_count}")

# 5. Convert dates for validation
df["Date of Admission"] = pd.to_datetime(
    df["Date of Admission"],
    errors="coerce"
)

df["Discharge Date"] = pd.to_datetime(
    df["Discharge Date"],
    errors="coerce"
)

# 6. Invalid dates
invalid_admission_dates = df["Date of Admission"].isna().sum()
invalid_discharge_dates = df["Discharge Date"].isna().sum()

print(f"Invalid admission dates: {invalid_admission_dates}")
print(f"Invalid discharge dates: {invalid_discharge_dates}")

# 7. Discharge before admission
invalid_date_order = (
    df["Discharge Date"] < df["Date of Admission"]
).sum()

print(f"Discharge before admission: {invalid_date_order}")

# 8. Calculate length of stay
df["Length of Stay"] = (
    df["Discharge Date"] -
    df["Date of Admission"]
).dt.days

negative_los = (df["Length of Stay"] < 0).sum()

print(f"Negative length of stay: {negative_los}")
# 9. Inspect negative billing records
print("\n=== NEGATIVE BILLING RECORDS ===")

negative_billing = df[df["Billing Amount"] < 0]

print(negative_billing[
    [
        "Name",
        "Age",
        "Medical Condition",
        "Insurance Provider",
        "Billing Amount",
        "Admission Type"
    ]
].head(20))
print("\n=== CHECK COMPLETE ===")
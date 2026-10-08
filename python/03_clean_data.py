import pandas as pd

# Load raw dataset
df = pd.read_csv("data/raw/healthcare_dataset.csv")

print(f"Original rows: {len(df)}")

# 1. Remove exact duplicate records
df_clean = df.drop_duplicates().copy()

print(f"Rows after removing duplicates: {len(df_clean)}")
print(f"Duplicates removed: {len(df) - len(df_clean)}")

# 2. Convert date columns
df_clean["Date of Admission"] = pd.to_datetime(
    df_clean["Date of Admission"],
    errors="coerce"
)

df_clean["Discharge Date"] = pd.to_datetime(
    df_clean["Discharge Date"],
    errors="coerce"
)

# 3. Create Length of Stay
df_clean["Length of Stay"] = (
    df_clean["Discharge Date"] -
    df_clean["Date of Admission"]
).dt.days

# 4. Flag invalid billing amounts
df_clean["Billing Amount Valid"] = (
    df_clean["Billing Amount"] >= 0
)

# 5. Flag invalid length of stay
df_clean["Length of Stay Valid"] = (
    df_clean["Length of Stay"] >= 0
)

# 6. Save processed dataset
output_path = "data/processed/healthcare_cleaned.csv"

df_clean.to_csv(
    output_path,
    index=False
)

print(f"\nCleaned dataset saved to: {output_path}")

print("\n=== FINAL QA FLAGS ===")
print(
    f"Invalid billing records: "
    f"{(~df_clean['Billing Amount Valid']).sum()}"
)

print(
    f"Invalid length-of-stay records: "
    f"{(~df_clean['Length of Stay Valid']).sum()}"
)
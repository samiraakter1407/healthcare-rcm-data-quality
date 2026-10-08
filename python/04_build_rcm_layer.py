import pandas as pd
import numpy as np

# Load cleaned healthcare data
df = pd.read_csv("data/processed/healthcare_cleaned.csv")

# Convert dates
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])

# Reproducibility
np.random.seed(42)

# Create claim IDs
df["claim_id"] = [
    f"CLM{i:07d}" for i in range(1, len(df) + 1)
]

# Use admission date as the service date
df["service_date"] = df["Date of Admission"]

# Generate submission date: 1–5 days after service
submission_days = np.random.randint(1, 6, size=len(df))

df["submission_date"] = (
    df["service_date"] +
    pd.to_timedelta(submission_days, unit="D")
)

# Generate claim status
statuses = ["Paid", "Denied", "Pending", "Rejected"]

df["claim_status"] = np.random.choice(
    statuses,
    size=len(df),
    p=[0.72, 0.15, 0.08, 0.05]
)

# Generate allowed amount
df["allowed_amount"] = np.where(
    df["Billing Amount"] >= 0,
    df["Billing Amount"] * np.random.uniform(
        0.70, 0.95, size=len(df)
    ),
    np.nan
)

# Generate paid amount
df["paid_amount"] = np.where(
    df["claim_status"] == "Paid",
    df["allowed_amount"] * np.random.uniform(
        0.80, 1.00, size=len(df)
    ),
    0
)

# Generate payment date for paid claims
payment_days = np.random.randint(7, 46, size=len(df))

df["payment_date"] = np.where(
    df["claim_status"] == "Paid",
    df["submission_date"] +
    pd.to_timedelta(payment_days, unit="D"),
    pd.NaT
)

df["payment_date"] = pd.to_datetime(df["payment_date"])
df["payment_date"] = df["payment_date"].dt.strftime("%Y-%m-%d")
df["payment_date"] = df["payment_date"].fillna("\\N")

# Generate denial reasons
denial_reasons = [
    "Missing Documentation",
    "Eligibility Issue",
    "Coding Error",
    "Authorization Required"
]

df["denial_reason"] = np.where(
    df["claim_status"].isin(["Denied", "Rejected"]),
    np.random.choice(
        denial_reasons,
        size=len(df)
    ),
    None
)

# Select RCM fields
rcm_columns = [
    "claim_id",
    "Name",
    "Age",
    "Gender",
    "Medical Condition",
    "Doctor",
    "Hospital",
    "Insurance Provider",
    "service_date",
    "submission_date",
    "Billing Amount",
    "allowed_amount",
    "paid_amount",
    "claim_status",
    "payment_date",
    "denial_reason",
    "Admission Type",
    "Length of Stay",
    "Billing Amount Valid",
    "Length of Stay Valid"
]

rcm_df = df[rcm_columns].copy()

rcm_df["Billing Amount Valid"] = rcm_df["Billing Amount Valid"].astype(int)
rcm_df["Length of Stay Valid"] = rcm_df["Length of Stay Valid"].astype(int)

# Rename columns for SQL-friendly names
rcm_df = rcm_df.rename(columns={
    "Name": "patient_name",
    "Age": "patient_age",
    "Gender": "gender",
    "Medical Condition": "medical_condition",
    "Doctor": "doctor",
    "Hospital": "hospital",
    "Insurance Provider": "payer",
    "Billing Amount": "billed_amount",
    "Admission Type": "admission_type",
    "Length of Stay": "length_of_stay",
    "Billing Amount Valid": "billing_amount_valid",
    "Length of Stay Valid": "length_of_stay_valid"
})

# Save RCM dataset
output_path = "data/processed/rcm_claims.csv"

rcm_df.to_csv(
    output_path,
    index=False
)

print("=== RCM LAYER CREATED ===")
print(f"Claims created: {len(rcm_df):,}")
print(f"Output: {output_path}")

print("\n=== CLAIM STATUS DISTRIBUTION ===")
print(rcm_df["claim_status"].value_counts())

print("\n=== TOTAL BILLED ===")
print(f"${rcm_df['billed_amount'].sum():,.2f}")

print("\n=== TOTAL PAID ===")
print(f"${rcm_df['paid_amount'].sum():,.2f}")
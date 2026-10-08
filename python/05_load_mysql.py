import pandas as pd
import mysql.connector

# Load CSV
df = pd.read_csv("data/processed/rcm_claims.csv")

# Convert missing payment dates to None (SQL NULL)
df["payment_date"] = df["payment_date"].replace(r"^\\N$", None, regex=True)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter MySQL password: "),
    database="healthcare_rcm"
)

cursor = conn.cursor()

# Insert query
query = """
INSERT INTO claims (
    claim_id,
    patient_name,
    patient_age,
    gender,
    medical_condition,
    doctor,
    hospital,
    payer,
    service_date,
    submission_date,
    billed_amount,
    allowed_amount,
    paid_amount,
    claim_status,
    payment_date,
    denial_reason,
    admission_type,
    length_of_stay,
    billing_amount_valid,
    length_of_stay_valid
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# Prepare data
data = [
    tuple(None if pd.isna(value) else value for value in row)
    for row in df.itertuples(index=False, name=None)
]

# Insert records
cursor.executemany(query, data)

conn.commit()

print(f"Successfully inserted {cursor.rowcount:,} claims.")

cursor.close()
conn.close()
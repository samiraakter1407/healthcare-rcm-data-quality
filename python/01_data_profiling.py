import pandas as pd

# Load raw dataset
df = pd.read_csv("data/raw/healthcare_dataset.csv")

# Basic dataset information
print("\n=== DATASET SHAPE ===")
print(df.shape)

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

print("\n=== UNIQUE VALUES ===")
print(df.nunique())

print("\n=== NUMERIC SUMMARY ===")
print(df.describe())
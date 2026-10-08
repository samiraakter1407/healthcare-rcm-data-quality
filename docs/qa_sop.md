# Healthcare RCM Data Quality QA SOP

## 1. Purpose

This SOP defines the standard process for validating data quality in the Healthcare RCM dataset.

The objective is to identify data issues before the data is used for operational reporting, reconciliation, or analytics.

## 2. Scope

This process applies to the claims data stored in the `healthcare_rcm` MySQL database and the `claims` table.

## 3. QA Checks

The following validation checks are performed:

1. Missing Claim ID
2. Missing Patient Name
3. Invalid Patient Age
4. Negative Billed Amount
5. Payment Date Before Submission Date
6. Invalid Length of Stay

## 4. Standard QA Process

### Step 1 — Confirm Data Load

Verify that the expected number of claims exists in the database.

```sql
SELECT COUNT(*) AS total_claims
FROM claims;
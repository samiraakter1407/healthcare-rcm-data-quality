# Data Quality Rules

## Purpose

This document defines the data-quality validation rules used for the Healthcare RCM Data Operations project.

The rules are designed to identify data issues that could affect claim processing, reporting, reconciliation, or operational analysis.

## Data Quality Rules

| Rule ID | Validation Rule | Expected Result | Severity | Action |
|---|---|---:|---|---|
| DQ-001 | Claim ID must not be missing | 0 issues | Critical | Investigate immediately |
| DQ-002 | Patient name must not be missing | 0 issues | High | Investigate and correct |
| DQ-003 | Patient age must be between 0 and 120 | 0 issues | Medium | Investigate invalid records |
| DQ-004 | Billed amount must not be negative | 0 issues | High | Flag for investigation |
| DQ-005 | Payment date must not precede submission date | 0 issues | High | Investigate date sequence |
| DQ-006 | Length of stay validation must pass | 0 issues | Medium | Investigate invalid records |

## Exception Handling

Records that fail a data-quality rule should be flagged for investigation rather than automatically deleted.

For this project, negative billed amounts are retained because the original dataset may contain values that require operational review. In a real RCM environment, negative amounts could represent adjustments, reversals, credits, or other financial transactions and would require business-rule validation.

## Current QA Baseline

The current MySQL QA analysis identified:

- 54,966 total claims
- 0 missing claim IDs
- 0 missing patient names
- 0 invalid ages
- 106 negative billed amounts
- 0 payments before submission
- 0 length-of-stay validation failures

The 106 negative billed amounts are currently treated as a data-quality exception requiring investigation.

## Current QA Results

| Rule ID | Issue Count | Status |
|---|---:|---|
| DQ-001 | 0 | Pass |
| DQ-002 | 0 | Pass |
| DQ-003 | 0 | Pass |
| DQ-004 | 106 | Review |
| DQ-005 | 0 | Pass |
| DQ-006 | 0 | Pass |

### Summary

The current dataset passed five of the six defined validation rules.

The only exception is **DQ-004 (Billed amount is non-negative)**, with **106 records** containing negative billed amounts. These records are retained for investigation rather than deleted, preserving the audit trail.
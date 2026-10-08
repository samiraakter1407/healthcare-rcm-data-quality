-- Healthcare RCM SQL Analysis
-- Project: Healthcare Revenue Cycle Data Quality & Claims Analytics


-- 1. Claim status distribution
SELECT
    claim_status,
    COUNT(*) AS claim_count,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims),
        2
    ) AS percentage
FROM claims
GROUP BY claim_status
ORDER BY claim_count DESC;


-- 2. Payer-level financial summary
SELECT
    payer,
    COUNT(*) AS claim_count,
    ROUND(SUM(billed_amount), 2) AS total_billed,
    ROUND(SUM(paid_amount), 2) AS total_paid
FROM claims
GROUP BY payer
ORDER BY total_billed DESC;


-- 3. Denial rate by payer
SELECT
    payer,
    COUNT(*) AS total_claims,
    SUM(claim_status IN ('Denied', 'Rejected')) AS denied_claims,
    ROUND(
        SUM(claim_status IN ('Denied', 'Rejected')) * 100.0
        / COUNT(*),
        2
    ) AS denial_rate
FROM claims
GROUP BY payer
ORDER BY denial_rate DESC;


-- 4. Denial reasons
SELECT
    denial_reason,
    COUNT(*) AS denied_claims,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM claims
         WHERE claim_status IN ('Denied', 'Rejected')),
        2
    ) AS percentage
FROM claims
WHERE claim_status IN ('Denied', 'Rejected')
GROUP BY denial_reason
ORDER BY denied_claims DESC;


-- 5. Negative billing exceptions by payer
SELECT
    payer,
    COUNT(*) AS negative_billing_records,
    ROUND(SUM(billed_amount), 2) AS total_negative_billed
FROM claims
WHERE billed_amount < 0
GROUP BY payer
ORDER BY negative_billing_records DESC;


-- 6. Collection rate by payer
SELECT
    payer,
    ROUND(SUM(billed_amount), 2) AS total_billed,
    ROUND(SUM(paid_amount), 2) AS total_paid,
    ROUND(
        SUM(paid_amount) * 100.0
        / NULLIF(SUM(billed_amount), 0),
        2
    ) AS collection_rate
FROM claims
GROUP BY payer
ORDER BY collection_rate DESC;


-- 7. Payer denial ranking using a window function
SELECT
    payer,
    COUNT(*) AS total_claims,
    SUM(claim_status IN ('Denied', 'Rejected')) AS denied_claims,
    ROUND(
        SUM(claim_status IN ('Denied', 'Rejected')) * 100.0
        / COUNT(*),
        2
    ) AS denial_rate,
    RANK() OVER (
        ORDER BY
            SUM(claim_status IN ('Denied', 'Rejected')) * 100.0
            / COUNT(*) DESC
    ) AS denial_rank
FROM claims
GROUP BY payer
ORDER BY denial_rank;
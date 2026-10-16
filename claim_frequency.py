import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
DB_PATH = "./insurance.db"

query = """
SELECT
    CASE
        WHEN DrivAge < 25 THEN '18–24'
        WHEN DrivAge < 40 THEN '25–39'
        WHEN DrivAge < 60 THEN '40–59'
        ELSE '60+'
    END AS age_group,
    COUNT(*) AS policy_count,
    SUM(ClaimNb) AS total_claims,
    SUM(Exposure) AS total_exposure,
    1.0 * SUM(ClaimNb) / SUM(Exposure)
        AS claim_frequency
FROM policies
WHERE Exposure > 0
GROUP BY age_group
ORDER BY claim_frequency DESC;
"""

with sqlite3.connect(DB_PATH) as conn:
    result = pd.read_sql_query(query, conn)

print(result)
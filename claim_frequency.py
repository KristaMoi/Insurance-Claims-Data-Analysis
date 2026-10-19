import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
DB_PATH = "./insurance.db"

# keskimääräiset vahinkofrekvenssit
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
ORDER BY age_group ASC;
"""

with sqlite3.connect(DB_PATH) as conn:
    result = pd.read_sql_query(query, conn)

print(result)

# rajataan frequency-aineistosta 10000 riviä
# result = result.sample(n=10000, random_state=42)
# print("Rivimäärä rajatun aineiston jälkeen:", len(result))

# kuvaaja: vahinkofrekvenssi ikäryhmittäin
result.plot(
    x="age_group",
    y="claim_frequency",
    kind="bar",
    legend=False
)

plt.ylabel("Vahinkoja vakuutusvuotta kohti")
plt.xlabel("Kuljettajan ikäryhmä")
plt.title("Vahinkofrekvenssi ikäryhmittäin")
plt.tight_layout()
plt.savefig("./outputs/claims_by_age.png", dpi=150)
plt.show()
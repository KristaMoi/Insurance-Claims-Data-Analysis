import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
DB_PATH = "./insurance.db"

# keskimääräiset vahinkokustannukset
with sqlite3.connect(DB_PATH) as conn:
    sev_df = pd.read_sql_query(
        "SELECT ClaimAmount FROM claims;",
        conn
    )

# lasketaan tunnusluvut pandasilla
average_claim = sev_df["ClaimAmount"].mean()
print("Vahinkojen määrä:", sev_df["ClaimAmount"].count())
print("Kokonaiskorvaussumma:", sev_df["ClaimAmount"].sum())
print("Keskimääräinen vahinkokustannus:", average_claim)
print("Mediaani:", sev_df["ClaimAmount"].median())

# vahinkokustannukset ikäryhmittäin
query_by_age = """
SELECT
    CASE
        WHEN p.DrivAge < 25 THEN '18–24'
        WHEN p.DrivAge < 40 THEN '25–39'
        WHEN p.DrivAge < 60 THEN '40–59'
        ELSE '60+'
    END AS age_group,
    COUNT(*) AS claim_count,
    SUM(c.ClaimAmount) AS total_claim_amount,
    AVG(c.ClaimAmount) AS average_claim_amount
FROM claims c
JOIN policies p ON c.IDpol = p.IDpol
WHERE c.ClaimAmount IS NOT NULL
GROUP BY age_group
ORDER BY MIN(p.DrivAge);
"""

with sqlite3.connect(DB_PATH) as conn:
    age_result = pd.read_sql_query(query_by_age, conn)

print("\nVahinkokustannukset ikäryhmittäin:")
print(age_result.to_string(index=False))

# kuvaaja: keskimääräinen vahinkokustannus ikäryhmittäin
age_result.plot(
    x="age_group",
    y="average_claim_amount",
    kind="bar",
    legend=False
)

plt.axhline(
    y=average_claim,
    color="red",
    linestyle="--",
    label=f"Koko aineiston keskiarvo: {average_claim:.2f}"
)

plt.ylabel("Keskimääräinen vahinkokustannus")
plt.xlabel("Kuljettajan ikäryhmä")
plt.title("Keskimääräinen vahinkokustannus ikäryhmittäin")
plt.tight_layout()
plt.savefig("./outputs/claim_severity_by_age.png", dpi=150)
plt.show()
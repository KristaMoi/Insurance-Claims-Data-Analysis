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

average_claim = sev_df["ClaimAmount"].mean()
print("Vahinkojen määrä:", sev_df["ClaimAmount"].count())
print("Kokonaiskorvaussumma:", sev_df["ClaimAmount"].sum())
print("Keskimääräinen vahinkokustannus:", average_claim)
print("Mediaani:", sev_df["ClaimAmount"].median())

# vahinkokustannukset ikäryhmittäin
query_by_age = """
SELECT
    c.ClaimAmount,
    CASE
        WHEN p.DrivAge < 25 THEN '18–24'
        WHEN p.DrivAge < 40 THEN '25–39'
        WHEN p.DrivAge < 60 THEN '40–59'
        ELSE '60+'
    END AS age_group
FROM claims c
JOIN policies p ON c.IDpol = p.IDpol
WHERE c.ClaimAmount IS NOT NULL;
"""

with sqlite3.connect(DB_PATH) as conn:
    age_df = pd.read_sql_query(query_by_age, conn)

age_result = (
    age_df
    .groupby("age_group")
    .agg(
            claim_count=("ClaimAmount", "count"),
            total_claim_amount=("ClaimAmount", "sum"),
            average_claim_amount=("ClaimAmount", "mean"),
            median_claim_amount=("ClaimAmount", "median")
        )
        .reset_index()
)

print(age_result)

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
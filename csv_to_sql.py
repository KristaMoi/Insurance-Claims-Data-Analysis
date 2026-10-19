import sqlite3
import pandas as pd

# luetaan aineistot
freq_df = pd.read_csv("data/freMTPL2freq.csv")
sev_df = pd.read_csv("data/freMTPL2sev.csv")

for df in [freq_df, sev_df]:
    print("Alkuperäinen rivimäärä:", len(df))

    # tarkistetaan puuttuvat arvot
    missing_values = df.isna()
    print("Puuttuvia arvoja:", missing_values.sum().sum())
    if missing_values.sum().sum() > 0:
         df.dropna(inplace=True)

# tietokanta
DB_PATH = "./insurance.db"
with sqlite3.connect(DB_PATH) as conn:
    freq_df.to_sql(
        "policies",
        conn,
        if_exists="replace",
        index=False
    )

    sev_df.to_sql(
        "claims",
        conn,
        if_exists="replace",
        index=False
    )

print(f"Tietokanta luotu: {DB_PATH}")
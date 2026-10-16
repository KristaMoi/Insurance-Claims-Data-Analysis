import sqlite3
import pandas as pd

# luetaan aineisto
df = pd.read_csv("freMTPL2freq.csv")
print("Alkuperäinen rivimäärä:", len(df))

# tarkistetaan puuttuvat arvot
missing_values = df.isna()
print("Puuttuvia arvoja:", missing_values.sum().sum())

# rajataan aineistosta 10000 riviä
df = df.sample(n=10000, random_state=42)
print("Rivimäärä rajatun aineiston jälkeen:", len(df))

# tietokanta
DB_PATH = "./insurance.db"
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        "policies",
        conn,
        if_exists="replace",
        index=False
    )

print(f"Tietokanta luotu: {DB_PATH}")
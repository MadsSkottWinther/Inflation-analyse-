import requests
import pandas as pd
import sqlite3
import io

# Hent dansk forbrugerprisindeks fra Danmarks Statistik
# VAREGR=000000: alle varer samlet
# ENHED=300: aarlig inflation i procent
# Tid=*: alle tidspunkter
url = "https://api.statbank.dk/v1/data/PRIS111/CSV?lang=da&VAREGR=000000&ENHED=300&Tid=*"

response = requests.get(url)
response.encoding = "utf-8"

df = pd.read_csv(io.StringIO(response.text), sep=";")

print("Kolonner:", df.columns.tolist())
print(df.head(10))
print(f"\nHentet {len(df)} raekker")

conn = sqlite3.connect("dst_data.db")
df.to_sql("prisindeks", conn, if_exists="replace", index=False)
print("\nData gemt i dst_data.db")
conn.close()

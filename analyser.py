import sqlite3
import pandas as pd

conn = sqlite3.connect("dst_data.db")

# 1. Se de seneste 12 maaneder
query1 = """
SELECT TID, INDHOLD as inflation_pct
FROM prisindeks
WHERE INDHOLD != '..'
ORDER BY TID DESC
LIMIT 12
"""
print("=== Seneste 12 maaneder (inflation %) ===")
print(pd.read_sql(query1, conn))

# 2. Gennemsnit per aar
query2 = """
SELECT 
    SUBSTR(TID, 1, 4) AS aar,
    ROUND(AVG(CAST(REPLACE(INDHOLD, ',', '.') AS FLOAT)), 2) AS gns_inflation
FROM prisindeks
WHERE INDHOLD != '..'
GROUP BY aar
ORDER BY aar DESC
LIMIT 10
"""
print("\n=== Gennemsnitlig inflation per aar ===")
print(pd.read_sql(query2, conn))

# 3. Hoejeste inflation nogensinde
query3 = """
SELECT TID, INDHOLD as inflation_pct
FROM prisindeks
WHERE INDHOLD != '..'
ORDER BY CAST(REPLACE(INDHOLD, ',', '.') AS FLOAT) DESC
LIMIT 5
"""
print("\n=== Top 5 hoejeste inflation ===")
print(pd.read_sql(query3, conn))

conn.close()


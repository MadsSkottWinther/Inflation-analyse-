import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect("dst_data.db")

df = pd.read_sql("""
    SELECT TID, CAST(REPLACE(INDHOLD, ',', '.') AS FLOAT) AS inflation
    FROM prisindeks
    WHERE INDHOLD != '..'
    ORDER BY TID
""", conn)
conn.close()

df["dato"] = pd.to_datetime(df["TID"].str.replace("M", "-"), format="%Y-%m")

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df["dato"], df["inflation"], color="#003366", linewidth=1.5)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.fill_between(df["dato"], df["inflation"], 0,
                where=(df["inflation"] > 0), alpha=0.15, color="#003366")

top = df.loc[df["inflation"].idxmax()]
ax.annotate(f'Energikrise\n{top["inflation"]}%',
            xy=(top["dato"], top["inflation"]),
            xytext=(top["dato"] - pd.DateOffset(years=2), top["inflation"] - 1.5),
            arrowprops=dict(arrowstyle="->", color="red"),
            fontsize=10, color="red")

ax.set_title("Dansk inflation 2001-2025 (aar-over-aar %)", fontsize=14, fontweight="bold")
ax.set_xlabel("Aar")
ax.set_ylabel("Inflation (%)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("inflation_graf.png", dpi=150)
plt.show()
print("Graf gemt som inflation_graf.png")

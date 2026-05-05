import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Hent data siden 2024
start = "2024-01-01"

omxc25 = yf.download("^OMXC25", start=start, auto_adjust=True)["Close"]
sp500  = yf.download("^GSPC",   start=start, auto_adjust=True)["Close"]

# Indekser til 100 ved start saa de kan sammenlignes
omxc25_idx = omxc25 / omxc25.iloc[0] * 100
sp500_idx  = sp500  / sp500.iloc[0]  * 100

# Graf
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(omxc25_idx.index, omxc25_idx, label="OMX Copenhagen 25 (DK)", color="#003366", linewidth=2)
ax.plot(sp500_idx.index,  sp500_idx,  label="S&P 500 (USA)",          color="#C8102E", linewidth=2)

ax.axhline(100, color="gray", linewidth=0.8, linestyle="--")

ax.set_title("Dansk vs. amerikansk aktiemarked siden 2024 (indekseret, start = 100)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Dato")
ax.set_ylabel("Indeks (start = 100)")
ax.legend(fontsize=11)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.grid(axis="y", alpha=0.3)
plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig("aktiemarked.png", dpi=150)
plt.show()

# Udskriv konkrete afkasttal
afkast_dk  = (float(omxc25.iloc[-1].squeeze()) / float(omxc25.iloc[0].squeeze()) - 1) * 100
afkast_usa = (float(sp500.iloc[-1].squeeze())  / float(sp500.iloc[0].squeeze())  - 1) * 100

print(f"\nAfkast siden januar 2024:")
print(f"  OMX Copenhagen 25: {afkast_dk:.1f}%")
print(f"  S&P 500:           {afkast_usa:.1f}%")
if afkast_usa > afkast_dk:
    print(f"\n  S&P 500 har outperformet OMX C25 med {afkast_usa - afkast_dk:.1f} procentpoint")
else:
    print(f"\n  OMX C25 har outperformet S&P 500 med {afkast_dk - afkast_usa:.1f} procentpoint")

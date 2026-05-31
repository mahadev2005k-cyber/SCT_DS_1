import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── STEP 1: Load the dataset ─────────────────────────────────────
df = pd.read_csv('population.csv', skiprows=4)
print("Dataset loaded! Shape:", df.shape)
print("Columns:", df.columns.tolist()[:6])

# ── STEP 2: Clean — remove regional aggregates ───────────────────
exclude = ['World','Arab World','Africa','Asia','Europe','OECD',
           'income','IDA','IBRD','Euro','Pacific','Caribbean',
           'Middle','South Asia','North America','Latin']

mask = ~df['Country Name'].apply(
    lambda x: any(kw.lower() in str(x).lower() for kw in exclude)
)
countries = df[mask].copy()
print("Countries after filtering:", len(countries))

# ── STEP 3: Get 2023 population data ─────────────────────────────
pop2023 = countries[['Country Name', '2023']].copy()
pop2023['2023'] = pd.to_numeric(pop2023['2023'], errors='coerce')
pop2023 = pop2023.dropna()
pop2023 = pop2023.sort_values('2023', ascending=False).head(20)
pop2023['Population (Billions)'] = pop2023['2023'] / 1e9

# ── CHART 1: Bar Chart — Top 20 Countries ────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))

colors = ['#e74c3c' if c == 'India' else
          '#3498db' if c == 'China' else
          '#2ecc71' for c in pop2023['Country Name']]

bars = ax.bar(pop2023['Country Name'],
              pop2023['Population (Billions)'],
              color=colors, edgecolor='white')

ax.set_title('Top 20 Most Populous Countries (2023)',
             fontsize=16, fontweight='bold')
ax.set_xlabel('Country', fontsize=12)
ax.set_ylabel('Population (Billions)', fontsize=12)
ax.tick_params(axis='x', rotation=45)
plt.xticks(ha='right', fontsize=9)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines[['top','right']].set_visible(False)

# Add number labels on top of each bar
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.01,
            f'{h:.2f}B', ha='center', va='bottom', fontsize=7)

plt.tight_layout()
plt.savefig('chart1_bar.png', dpi=150)
plt.show()
print("Chart 1 saved!")

# ── CHART 2: Histogram — Population Distribution ─────────────────
pop_all = countries[['Country Name', '2023']].copy()
pop_all['2023'] = pd.to_numeric(pop_all['2023'], errors='coerce')
pop_all = pop_all.dropna()
pop_all['Pop_Millions'] = pop_all['2023'] / 1e6

fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(pop_all['Pop_Millions'], bins=30,
        color='#3498db', edgecolor='white', alpha=0.85)

ax.set_title('Distribution of Countries by Population Size (2023)',
             fontsize=15, fontweight='bold')
ax.set_xlabel('Population (Millions)', fontsize=12)
ax.set_ylabel('Number of Countries', fontsize=12)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('chart2_histogram.png', dpi=150)
plt.show()
print("Chart 2 saved!")

# ── CHART 3: Line Chart — Population Growth Over Time ────────────
big5 = ['India', 'China', 'United States', 'Indonesia', 'Pakistan']
years = [str(y) for y in range(1960, 2024)]
colors5 = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']

fig, ax = plt.subplots(figsize=(13, 6))

for country, color in zip(big5, colors5):
    row = df[df['Country Name'] == country]
    if not row.empty:
        vals = pd.to_numeric(row[years].values[0], errors='coerce') / 1e9
        ax.plot(range(1960, 2024), vals,
                label=country, color=color, linewidth=2.5)

ax.set_title('Population Growth (1960–2023) — Top 5 Countries',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Population (Billions)', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.3, linestyle='--')
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('chart3_growth.png', dpi=150)
plt.show()
print("Chart 3 saved!")

print("\n✅ All done! Check your folder for the 3 chart images.")
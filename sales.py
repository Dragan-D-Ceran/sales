import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: make plots look nicer
sns.set(style="whitegrid")

# %matplotlib inline  # Removed because it's only for Jupyter notebooks

df = pd.read_csv("/Users/draganceran/Downloads/Sales Analysis/Sales.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

print(df.head())

# --- Data Cleaning Steps ---
# 1. Remove rows with missing or NaN values
cleaned_df = df.dropna()

# 2. Remove duplicate rows
cleaned_df = cleaned_df.drop_duplicates()

# 3. Fix data types (example: convert 'Order Date' to datetime, 'Quantity Ordered' and 'Price Each' to numeric if present)
if 'Order Date' in cleaned_df.columns:
    cleaned_df['Order Date'] = pd.to_datetime(cleaned_df['Order Date'], errors='coerce')
    cleaned_df = cleaned_df.dropna(subset=['Order Date'])
if 'Quantity Ordered' in cleaned_df.columns:
    cleaned_df['Quantity Ordered'] = pd.to_numeric(cleaned_df['Quantity Ordered'], errors='coerce')
    cleaned_df = cleaned_df.dropna(subset=['Quantity Ordered'])
if 'Price Each' in cleaned_df.columns:
    cleaned_df['Price Each'] = pd.to_numeric(cleaned_df['Price Each'], errors='coerce')
    cleaned_df = cleaned_df.dropna(subset=['Price Each'])

# 4. Trim whitespace from string columns
for col in cleaned_df.select_dtypes(include=['object']).columns:
    cleaned_df[col] = cleaned_df[col].str.strip()

# Show info and first 5 rows of cleaned data
print("\nCleaned DataFrame info:")
print(cleaned_df.info())
print("\nFirst 5 rows of cleaned data:")
print(cleaned_df.head())

daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(daily_revenue['Date'], daily_revenue['Revenue'])
plt.title("Daily Revenue Over Time")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------
# 2. Revenue by Month
# --------------------------
df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

monthly_revenue = df.groupby('YearMonth')['Revenue'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_revenue, x='YearMonth', y='Revenue', marker='o')
plt.title("Monthly Revenue Over Time")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------
# 3. Revenue by Year
# --------------------------
yearly_revenue = df.groupby('Year')['Revenue'].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(data=yearly_revenue, x='Year', y='Revenue')
plt.title("Yearly Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# --------------------------
# 4. Seasonal Patterns (Avg Revenue by Month)
# --------------------------
# First: fix 'Month' format if needed (capitalize first letter)
df['Month'] = df['Month'].str.capitalize()

# Convert month names to numbers
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
df['Month_Num'] = df['Month'].apply(lambda x: month_order.index(x) + 1)

# Calculate average revenue by month number
monthly_avg = df.groupby('Month_Num')['Revenue'].mean().reset_index()

# Add short month labels
monthly_avg['Month'] = monthly_avg['Month_Num'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))

plt.figure(figsize=(10, 5))
sns.barplot(data=monthly_avg.sort_values('Month_Num'), x='Month', y='Revenue')
plt.title("Average Revenue by Month (Seasonal Patterns)")
plt.xlabel("Month")
plt.ylabel("Average Revenue")
plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: make plots look nicer
sns.set(style="whitegrid")

# %matplotlib inline  # Removed because it's only for Jupyter notebooks

df = pd.read_csv("/Users/draganceran/Downloads/Sales Analysis/Sales.csv")

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

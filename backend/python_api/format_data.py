import pandas as pd
import os

# Paths
input_csv = r"c:\Users\HP\dsaelantigrav\backend\c_core\data\pois_raw.csv"
output_csv = r"c:\Users\HP\dsaelantigrav\backend\c_core\data\pois.csv"

# Read with encoding handling
try:
    df = pd.read_csv(input_csv, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(input_csv, encoding='latin-1')

# Ensure ID column is present and valid
if 'id' not in df.columns:
    df.insert(0, 'id', range(1, 1 + len(df)))
else:
    df['id'] = range(1, 1 + len(df)) # Re-index to ensure clean sequence

# Clean data for simple C parsing (remove commas and quotes from strings)
def clean_text(text):
    if isinstance(text, str):
        return text.replace(',', ' ').replace('"', '').replace("'", "")
    return text

df['name'] = df['name'].apply(clean_text)
df['type'] = df['type'].apply(clean_text)

# Save
df.to_csv(output_csv, index=False)
print(f"Processed {len(df)} POIs and saved to {output_csv}")

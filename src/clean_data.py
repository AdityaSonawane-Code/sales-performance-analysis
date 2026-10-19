
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*.xls")) + list(RAW_DIR.glob("*.xlsx"))

if not files:
    raise FileNotFoundError("No Excel dataset found in data/raw.")

file_path = next(
    (f for f in files if "superstore" in f.name.lower()),
    files[0]
)

# Read the Orders sheet when available
excel_file = pd.ExcelFile(file_path)
sheet_name = "Orders" if "Orders" in excel_file.sheet_names else excel_file.sheet_names[0]
df = pd.read_excel(file_path, sheet_name=sheet_name)

print("Original dataset shape:", df.shape)

# Standardize column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# Remove duplicate rows
duplicates_removed = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Convert date columns
for col in ["order_date", "ship_date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Convert numeric columns
numeric_columns = ["sales", "quantity", "discount", "profit"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows missing essential analysis fields
essential_columns = [
    col for col in ["order_date", "sales", "profit", "category"]
    if col in df.columns
]
rows_before = len(df)

if essential_columns:
    df = df.dropna(subset=essential_columns).copy()

rows_removed_missing = rows_before - len(df)

# Save the cleaned dataset
output_file = PROCESSED_DIR / "superstore_cleaned.csv"
df.to_csv(output_file, index=False)

print("\nCLEANING SUMMARY")
print("Duplicates removed:", duplicates_removed)
print("Rows removed for missing essential values:", rows_removed_missing)
print("Cleaned dataset shape:", df.shape)
print("Remaining missing values:")
print(df.isnull().sum().to_string())
print("\nSaved cleaned dataset to:", output_file)

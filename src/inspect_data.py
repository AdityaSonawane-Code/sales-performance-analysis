from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"

files = list(DATA_DIR.glob("*.xls")) + list(DATA_DIR.glob("*.xlsx"))

if not files:
    raise FileNotFoundError("No Excel dataset found in data/raw.")

file_path = next(
    (f for f in files if "superstore" in f.name.lower()),
    files[0]
)

df = pd.read_excel(file_path)

print("DATASET:", file_path.name)
print("\nSHAPE (rows, columns):", df.shape)
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:", df.duplicated().sum())

print("\nFIRST FIVE ROWS:")
print(df.head())

print("\nNUMERICAL SUMMARY:")
print(df.describe(include="all").transpose())
from src.data_loader import load_initial_dataset


df = load_initial_dataset()

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nTarget distribution:")
print(df["converted"].value_counts())
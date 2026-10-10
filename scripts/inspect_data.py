import pandas as pd
df = pd.read_csv("./data/raw/banking77/train.csv")
print(df.head())
df.info()
print(f"Missing values count: {df.isna().sum().sum()}")
print(f"Duplicate rows count: {df.duplicated().sum()}")
print(f"Duplicate texts count: {df.duplicated(subset=['text']).sum()}")
print(f"Examples per class: {df['category'].value_counts()}")
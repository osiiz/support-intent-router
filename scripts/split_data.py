import pandas as pd
from pathlib import Path
import hashlib, json, platform
from sklearn.model_selection import train_test_split
from importlib.metadata import version

source_path = Path("./data/raw/banking77/train.csv")
seed = 42
holdout_size = 0.3
calibration_size = 0.5

df = pd.read_csv(source_path)

train_df, holdout_df = train_test_split(df, test_size=holdout_size, stratify=df['category'], 
                            random_state=seed, shuffle=True)
develop_df, calibration_df = train_test_split(holdout_df, test_size=calibration_size, stratify=holdout_df['category'],
                            random_state=seed, shuffle=True)

print(f"Train set size: {len(train_df)}, category distribution: {train_df['category'].value_counts()}")
print(f"Develop set size: {len(develop_df)}, category distribution: {develop_df['category'].value_counts()}")
print(f"Calibration set size: {len(calibration_df)}, category distribution: {calibration_df['category'].value_counts()}")

assert len(train_df) + len(develop_df) + len(calibration_df) == len(df), "The sum of the splits does not match the original dataset size."
assert set(train_df['category'].unique()) == set(develop_df['category'].unique()) == set(calibration_df['category'].unique()), "The subsets contain the same categories"
assert set(train_df.index) & set(develop_df.index) == set() and set(train_df.index) & set(calibration_df.index) == set() and set(develop_df.index) & set(calibration_df.index) == set(), "Each pair of subset index should have no intersection"
assert set(train_df.index) | set(develop_df.index) | set(calibration_df.index) == set(df.index), "The union of the subset indices should match the original dataset indices"

output_dir = Path("./data/processed/banking77")
output_dir.mkdir(parents=True, exist_ok=True)

splits = {
    "train": train_df,
    "develop": develop_df,
    "calibration": calibration_df
}  

for name, subset in splits.items():
    output_path = output_dir / f"{name}.csv"
    subset.to_csv(output_path, index=True, index_label="source_row_id", encoding="utf-8")
    reloaded = pd.read_csv(output_path, index_col="source_row_id")
    assert reloaded.equals(subset), f"{name} changed during CSV export."
    print(f"Saved {name}: {len(subset)} rows to {output_path}")


manifest = {
    "schema_version": "1.0",
    "source":{
        "path": source_path.as_posix(),
        "url": (
            "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/"
            "9d081458ff52e53cf7e848f414e6e9344e4e6696/banking_data/train.csv"
        ),
        "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
    },
    "split_settings": {
        "seed": seed,
        "holdout_fraction": holdout_size,
        "calibration_fraction_of_holdout": calibration_size,
        "stratify_column": "category",
    },
    "versions": {
        "python": platform.python_version(),
        **{
            package: version(package) for package in ["pandas", "scikit-learn", "numpy", "scipy"]
        },
    },
    "subsets": {
        name: {
            "size": len(subset),
            "source_row_ids": subset.index.tolist(),
        }
        for name, subset in splits.items()
    },
}

manifest_path = Path("configs/banking77_split.json")
manifest_path.parent.mkdir(parents=True, exist_ok=True)
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
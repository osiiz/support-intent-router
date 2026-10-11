import json
from pathlib import Path

import pandas as pd


rows = []

for path in Path("results").glob("tfidf_logreg_*.json"):
    result = json.loads(path.read_text())
    metrics = result["metrics"]

    rows.append({
        "run": result["run_name"],
        "C": result["configuration"]["logistic_regression"]["C"],
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "errors": metrics["error_count"],
        "iterations": metrics["solver_iterations"],
    })

comparison = pd.DataFrame(rows).sort_values("C")

print(comparison.to_string(
    index=False,
    float_format=lambda value: f"{value:.4f}",
))
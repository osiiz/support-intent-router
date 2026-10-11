from pathlib import Path
import pandas as pd
from time import perf_counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, f1_score
import hashlib, json, platform, os, argparse
from importlib.metadata import version

data_dir = Path("data/processed/banking77")

train_df = pd.read_csv(data_dir / "train.csv", index_col="source_row_id")
develop_df = pd.read_csv(data_dir / "develop.csv", index_col="source_row_id")

parser = argparse.ArgumentParser()
parser.add_argument("--c", type=float, default=1.0, help="Inverse regularization strength for logistic regression")

args = parser.parse_args()

X_train, y_train = train_df["text"], train_df["category"]
X_develop, y_develop = develop_df["text"], develop_df["category"]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(
        C=args.c, solver="lbfgs", max_iter=1000,
    )),
])

print(f"Training model with C={args.c:g}...", flush=True)
started = perf_counter()

model.fit(X_train, y_train)

training_seconds = perf_counter() - started
print(f"Training completed in {training_seconds:.2f} seconds")

predictions = model.predict(X_develop)
accuracy = accuracy_score(y_develop, predictions)
macro_f1 = f1_score(y_develop, predictions, average="macro")

print(f"Development accuracy: {accuracy:.4f}")
print(f"Development macro-F1: {macro_f1:.4f}")
print(f"Vocabulary size: {len(model.named_steps['tfidf'].vocabulary_)}")
print(f"Solver iterations: {model.named_steps['classifier'].n_iter_[0]}")

evaluation_df = (develop_df.rename(columns={"category": "actual"}).assign(predicted=predictions))

errors = evaluation_df.loc[evaluation_df["actual"] != evaluation_df["predicted"]].copy()

print(f"Misclassified requests: {len(errors)} / {len(evaluation_df)}")

confusions = (errors.groupby(["actual", "predicted"]).size().sort_values(ascending=False).rename("count"))

print("Most frequent confusions (actual -> predicted):")
print(confusions.head(10).to_string())

sample_errors = errors.sample(n=min(10, len(errors)), random_state=42)

print("Sample errors:")
for source_row_id, row in sample_errors.iterrows():
    print(f"\nSource row: {source_row_id}")
    print(f"Text: {row['text']}")
    print(f"Actual: {row['actual']}")
    print(f"Predicted: {row['predicted']}")

report = classification_report(
    y_develop,
    predictions,
    output_dict=True,
    zero_division=0,
)

per_intent = pd.DataFrame(report).T.loc[
    model.classes_,
    ["precision", "recall", "f1-score", "support"],
]

print("\nLowest F1 scores by intent:")
print(
    per_intent
    .sort_values("f1-score")
    .head(10)
    .to_string(float_format=lambda value: f"{value:.3f}")
)

benchmark_seed = 42
warmup_calls = 20
texts = X_develop.sample(frac=1, random_state=benchmark_seed).tolist()

for text in texts[:warmup_calls]:
    model.predict([text])

durations_ms = []

for text in texts:
    request = [text]

    started = perf_counter()
    model.predict(request)
    elapsed_ms = (perf_counter() - started) * 1000

    durations_ms.append(elapsed_ms)

durations = pd.Series(durations_ms)

# Hardware identification
cpu_model = next(
    (
        line.split(":", 1)[1].strip()
        for line in Path("/proc/cpuinfo").read_text().splitlines()
        if line.startswith("model name")
    ),
    "unknown",
)

latency = {
    "method": "pipeline.predict",
    "unit": "milliseconds",
    "batch_size": 1,
    "request_concurrency": 1,
    "measured_calls": len(texts),
    "warmup_calls": warmup_calls,
    "shuffle_seed": benchmark_seed,
    "p50_ms": float(durations.quantile(0.50)),
    "p95_ms": float(durations.quantile(0.95)),
    "platform": platform.platform(),
    "cpu_model": cpu_model,
    "logical_cpus_visible": os.cpu_count(),
    "thread_control": "not overridden by benchmark",
}

print(f"\nInference latency p50: {latency['p50_ms']:.3f} ms")
print(f"Inference latency p95: {latency['p95_ms']:.3f} ms")

run_name = f"tfidf_logreg_c{args.c:g}"
split_manifest_path = Path("configs/banking77_split.json")

tfidf_params = model.named_steps["tfidf"].get_params()
classifier_params = model.named_steps["classifier"].get_params()

# JSON cannot store a Python type; record its name instead.
tfidf_params["dtype"] = tfidf_params["dtype"].__name__

result = {
    "schema_version": "1.0",
    "run_name": run_name,
    "evaluation_subset": "develop",
    "split_manifest": {
        "path": split_manifest_path.as_posix(),
        "sha256": hashlib.sha256(
            split_manifest_path.read_bytes()
        ).hexdigest(),
    },
    "versions": {
        "python": platform.python_version(),
        **{
            package: version(package)
            for package in ["pandas", "scikit-learn", "numpy", "scipy"]
        },
    },
    "configuration": {
        "tfidf": tfidf_params,
        "logistic_regression": classifier_params,
    },
    "metrics": {
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "error_count": len(errors),
        "train_rows": len(train_df),
        "development_rows": len(develop_df),
        "training_seconds": training_seconds,
        "vocabulary_size": len(
            model.named_steps["tfidf"].vocabulary_
        ),
        "solver_iterations": int(
            model.named_steps["classifier"].n_iter_[0]
        ),
    },
    "per_intent": per_intent.to_dict(orient="index"),
    "latency": latency,
}

result_path = Path("results") / f"{run_name}.json"
result_path.parent.mkdir(parents=True, exist_ok=True)
result_path.write_text(
    json.dumps(result, indent=2, allow_nan=False) + "\n",
    encoding="utf-8",
)

print(f"\nSaved experiment results to {result_path}")
# Support Intent Router

Building a support-request router that assigns known intents or sends requests to human review. Planned work includes confidence calibration and unsupported-request detection.

Status: data preparation and an initial TF-IDF baseline implemented. Development evaluation is available; calibration and the review demo are planned.

See [project notes](docs/project.md) for scope and decisions, and [progress](docs/progress.md) for current status and next steps.

Agent collaboration instructions live in [AGENTS.md](AGENTS.md).

With the experiment environment and local data splits prepared, run the baseline
from the repository root:

```bash
.venv/bin/python scripts/train_tf_idf.py
```

The [initial experiment record](results/tfidf_logreg_v1.json) contains model
settings, development metrics, and local inference latency measurements.

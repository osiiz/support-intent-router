# Progress

## Current status

Data preparation completed and verified on 2026-10-10. The first baseline
experiment is in progress. The initial TF-IDF plus logistic regression
experiment is complete: training, development evaluation, error inspection,
configuration export, and a local inference latency measurement are implemented.
The frozen-embedding comparison remains outstanding.

Completed:

- Inspected Banking77 training data: 10,003 rows, 77 intents, no missing cells,
  duplicate rows, or duplicate texts; class sizes range from 35 to 187.
- Declared the experiment dependencies in [pyproject.toml](../pyproject.toml).
- Created stratified train/develop/calibration splits of 7,002/1,500/1,501 rows
  using seed `42`, with source row IDs preserved in the local CSVs.
- Saved source provenance, split settings, installed versions, and exact row
  assignments in [the split manifest](../configs/banking77_split.json).
- Implemented [the initial TF-IDF training script](../scripts/train_tf_idf.py).
  Development accuracy is `0.8340`, macro-F1 is approximately `0.8286`, with
  249 errors out of 1,500 requests. Aggregate scores were reproduced in an agent
  run; the user inspected confusion pairs, sample errors, and per-intent metrics.
- Saved the initial configuration, full-precision metrics for all 77 intents,
  split provenance, dependency versions, and latency conditions in
  [the initial experiment record](../results/tfidf_logreg_v1.json).

Validation: rerunning `.venv/bin/python scripts/split_data.py` produced identical
CSV and manifest bytes. Independent checks confirmed the source fingerprint,
manifest row order, complete and disjoint source coverage, unchanged text and
labels, and all 77 intents in each subset. Declared dependency pins match the
installed environment. Git ignores the local source, processed data, and virtual
environment. Installation in a fresh environment has not been verified.

The complete training script also passed an agent run with temporary output
storage, preserving the user's saved record. Classification scores and all
per-intent metrics reproduced, source and split fingerprints matched, and the
1,500 latency samples and percentile calculations were verified. The saved local
measurement reports approximately 0.438 ms p50 and 0.633 ms p95 on an AMD Ryzen 5
3600X under WSL2. This measures an already-loaded pipeline with batch size one;
model loading and application overhead are excluded, and numerical library
threads are not controlled by the benchmark.

## Next step

Propose a commit for the completed initial TF-IDF experiment. Then compare a
small set of logistic regression `C` values, holding TF-IDF settings and splits
fixed and preserving the initial result. Follow the
[evaluation protocol](project.md#evaluation-protocol) for calibration and final
testing.

## Blockers

None.

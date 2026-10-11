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
- Completed a development sweep over logistic regression `C=0.1` and integer
  values `1` through `10`, with separate saved results and
  [a comparison script](../scripts/compare_tfidf.py). [C=0.1](../results/tfidf_logreg_c0.1.json)
  scored approximately `0.5818` macro-F1; the initial `C=1` scored `0.8286`;
  [C=10](../results/tfidf_logreg_c10.json) scored `0.8710`, with accuracy `0.8687`
  and 197 errors. Gains largely plateau around `C=4`. `C=9` also made 197 errors;
  its macro-F1 is only approximately `0.000184` below `C=10`.
- Checked all 11 saved records: configurations differ only in `C`, with matching
  versions, split fingerprints, and class supports. Aggregate scores agree with
  error counts and per-intent metrics. The user reports the computer was busy
  during the sweep; its timing measurements are unsuitable for a fair speed
  comparison. Classification results remain usable.

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

Propose a commit for the completed regularization sweep. `C=10` is the best
tested TF-IDF setting by development macro-F1; using it as the comparison
candidate is proposed. Choose a frozen sentence encoder for the second baseline
and use comparable, controlled timing conditions when measuring both models.
Follow the
[evaluation protocol](project.md#evaluation-protocol) for calibration and final
testing.

## Blockers

None.

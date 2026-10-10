# Progress

## Current status

Data preparation completed and verified on 2026-10-10. The first baseline
experiment is in progress; model training has not started. The user writes the
implementation and owns commits. Planning scaffold commit: `6f0f259`
(`Initial commit`).

Completed:

- Inspected Banking77 training data: 10,003 rows, 77 intents, no missing cells,
  duplicate rows, or duplicate texts; class sizes range from 35 to 187.
- Declared pandas `3.0.6` and scikit-learn `1.9.1` in the `experiment` dependency
  group in [pyproject.toml](../pyproject.toml).
- Created stratified train/develop/calibration splits of 7,002/1,500/1,501 rows
  using seed `42`, with source row IDs preserved in the local CSVs.
- Saved source provenance, split settings, installed versions, and exact row
  assignments in [the split manifest](../configs/banking77_split.json).

Validation: rerunning `.venv/bin/python scripts/split_data.py` produced identical
CSV and manifest bytes. Independent checks confirmed the source fingerprint,
manifest row order, complete and disjoint source coverage, unchanged text and
labels, and all 77 intents in each subset. Declared dependency pins match the
installed environment. Git ignores the local source, processed data, and virtual
environment. Installation in a fresh environment has not been verified.

## Next step

Guide the user through a TF-IDF plus logistic regression pipeline: fit on the
model-training subset and report development accuracy and macro-F1. Then save
experiment settings and results and measure inference latency. Leave calibration
and the official test split reserved for their agreed purposes.

## Blockers

No current blocker. Normal sandboxed shell execution and
workspace reads were verified on 2026-10-10 after the user's WSL helper-directory
mount workaround. Model training and evaluation have not been run.

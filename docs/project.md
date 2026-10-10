# Project plan

## Purpose

Build a support-request router that assigns known intents or sends requests to
human review. Routing is not request resolution. Confidence and escalation
behavior must be evaluated; they are not guarantees of correctness.

The portfolio goal is a reproducible comparison showing whether a small, fast
model is sufficient and what a pretrained representation adds.

## Agreed scope and decisions

- Start with [PolyAI's Banking77 dataset](https://huggingface.co/datasets/PolyAI/banking77)
  for supported-intent classification. Unsupported requests need separate data
  because the supported-intent benchmark does not establish rejection behavior.
- Compare TF-IDF plus logistic regression with frozen sentence embeddings plus
  logistic regression. Keeping the classifier family the same makes the
  representation comparison easier to interpret.
- Complete a reproducible baseline experiment first. Add calibration, rejection
  policies, and the review demo in later milestones so the first result remains
  focused and reviewable.
- Prefer simple implementations. Add dependencies and infrastructure only when
  required by the current milestone.

## Milestones

1. **Reproducible baseline experiment:** implement dataset loading and split
   creation, train both baselines, and save configurations, development results,
   error analysis, and inference timing. Document how to reproduce the comparison.
2. **Calibration and selective routing:** evaluate confidence calibration, tune
   escalation on development data, and measure routing error versus coverage.
   Construct distinct unsupported-request development and final challenge sets.
3. **Review demo:** accept a pasted request and show its suggested intent,
   confidence, and review decision. Provide a small queue where a reviewer can
   assign an intent or mark a request unsupported.

## Evaluation protocol

- Create stratified model-training, development, and calibration subsets from the
  official training split. Record exact sizes, seeds, split identifiers, and
  purposes before running experiments. These values are not chosen yet.
- Fit learned preprocessing and classifiers on model-training data only. Use
  development data for model and policy selection, and the separate calibration
  subset to fit calibration.
- Use the same splits for both model families. Freeze model configurations,
  calibration choices, and escalation thresholds before final evaluation.
- Reserve the official test split for final supported-intent evaluation. The
  baseline milestone should first produce a development comparison; keep final
  testing reserved while later calibration and routing choices remain open.
- Keep unsupported-request development examples separate from final challenge
  examples. Record provenance, labeling rules, and any synthetic generation.
  Distinguish unsupported requests from ambiguous and multi-intent requests.
- Report supported-intent accuracy and macro-F1, calibration behavior, routing
  error versus coverage, and unsupported acceptance and supported rejection rates
  separately. Coverage means the proportion automatically routed, not resolved.
- Include preprocessing and encoding in inference latency. Record hardware,
  batching, warm-up, and measurement conditions.
- Save dataset and encoder revisions, dependency versions, configuration, seeds,
  and results so the comparison can be reproduced. Keep raw data and generated
  model artifacts out of Git; retain shareable configurations and metrics.

## Proposals and open decisions

The application stack, encoder, deployment, project license, and operating target
remain undecided. No model performance, latency, or coverage target has been
established.

Proposals to assess in later milestones:

- Start rejection with a confidence threshold and compare calibration before and
  after fitting a calibrator.
- Include both clearly unrelated and unsupported banking requests in the challenge
  data. Evaluate supported-request typos and paraphrases separately as robustness.
- Use reliability plots, log loss, p50/p95 latency, and uncertainty estimates to
  supplement the core results.

## Repository practice

Keep the README short until there is a working implementation. Store lasting
decisions here and session status in [progress.md](progress.md). Never check in
credentials, private customer messages, downloaded datasets, local environments,
or generated model artifacts.

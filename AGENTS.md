# Agent guidance

## Context

Read `docs/project.md` and `docs/progress.md` before making changes. Keep the README minimal until there is a working implementation.

This system routes requests to known intents or human review. Routing does not mean resolving a request. Describe confidence and escalation as evaluated behavior, not guarantees.

## Working practices

- Make small, focused changes that advance the current milestone.
- Prefer simple, reproducible implementations. Add dependencies and infrastructure only when needed.
- Record lasting decisions and their reasons in `docs/project.md`. Distinguish agreed choices from proposals.
- Update `docs/progress.md` when work is completed, the next step changes, or a blocker affects future sessions. Keep it concise.
- Preserve unrelated user changes.
- The user is responsible for making commits. Agents must not commit or push on
  their own. When a meaningful feature or milestone is completed and verified,
  propose a commit to the user with a suggested message and a short summary of
  the changes and checks. Do not stage files unless the user explicitly asks.
- Run checks appropriate to the change and report checks that could not run. Documentation-only changes need accuracy and link review, not new tests.
- Do not invent results, completed checks, or setup commands that have not been verified.
- Do not commit credentials, private customer messages, local environments, downloaded datasets, or generated model artifacts. Add ignore rules when introducing these files.

## Modeling and evaluation

- Start with TF-IDF plus logistic regression, then frozen sentence embeddings plus logistic regression.
- Fit preprocessing on training data only. Reserve the official test split for final evaluation.
- Create held-out development and calibration subsets from training data. Record split sizes, seeds, and purposes.
- Tune escalation thresholds using development data and freeze them before final testing.
- Keep unsupported-request development examples separate from final challenge examples. Document provenance, labeling rules, and synthetic generation.
- Evaluate supported-intent classification, calibration, selective routing, and unsupported-request detection separately.
- Include preprocessing and encoding in inference latency. Record hardware and measurement conditions.
- Save experiment configuration and results so the comparison can be reproduced.

## Current scope

The first milestone is a reproducible baseline experiment. Calibration, rejection policies, and the review demo follow. The application stack, encoder, deployment, license, and operating target remain open decisions.

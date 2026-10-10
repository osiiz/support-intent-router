# Agent guidance

## Context

Read [the project plan](docs/project.md) and [current progress](docs/progress.md)
before making changes. Follow the agreed scope and evaluation protocol in the
project plan; keep proposed choices distinct from agreed decisions.

## Documentation responsibilities

- `README.md`: public introduction, implemented capabilities, and entry points to
  the project documentation. Keep it minimal while the implementation develops.
- `docs/project.md`: purpose, scope, milestones, lasting technical decisions and
  their reasons, evaluation protocol, and open proposals. Keep agent behavior and
  repository housekeeping rules here in `AGENTS.md` instead.
- `docs/progress.md`: completed work, verification evidence, the next step, and
  active blockers. Keep it concise; do not duplicate the project plan or retain
  resolved setup issues as blockers.
- `pyproject.toml` and experiment manifests: exact dependency declarations and
  machine-readable experiment settings. Link to them from prose rather than
  maintaining duplicate version lists.
- Update documentation for meaningful milestones, lasting decisions, changes to
  the next step, or blockers that affect future sessions. Do not update it for
  every small implementation step or review exchange.

## Guided implementation

The user writes the implementation to understand the whole project. Explain
choices, review and run the user's code, and suggest focused corrections. Code
examples in conversation are welcome; do not write or edit implementation files
unless the user explicitly asks. Documentation edits are allowed within the
responsibilities above.

## Working practices

- Make small, focused changes that advance the current milestone.
- Prefer simple, reproducible implementations. Add dependencies and infrastructure only when needed.
- Preserve unrelated user changes.
- The user is responsible for making commits. Agents must not commit or push on
  their own. When a meaningful feature or milestone is completed and verified,
  propose a commit to the user with a suggested message and a short summary of
  the changes and checks. Do not stage files unless the user explicitly asks.
- Run checks appropriate to the change and report checks that could not run. Documentation-only changes need accuracy and link review, not new tests.
- Do not invent results, completed checks, or setup commands that have not been verified.
- Do not commit credentials, private customer messages, local environments, downloaded datasets, or generated model artifacts. Add ignore rules when introducing these files.
- Run the current data scripts from the repository root, because their paths are
  relative to that directory.

## Reporting

Describe confidence and escalation as evaluated behavior, not guarantees. Routing
does not mean resolving a request. Report only capabilities and results supported
by the implementation and completed checks.

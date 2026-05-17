# Contributing to AOS-spec

Thank you for helping improve AOS. Small, focused contributions are easier to review than large rewrites.

## What we're looking for

- **Use case reports** — What kind of agent behavior are you trying to constrain?
- **Spec feedback** — Is any section unclear or ambiguous?
- **Implementation examples** — Have you implemented AOS-style hooks or CI gates in your own project?

## How to contribute

1. Open an issue with your question, use case, or suggestion (templates are available under `.github/ISSUE_TEMPLATE/`).
2. For normative changes to the specification, open a pull request editing `AOS-v0.1.md` with clear rationale and minimal diff.
3. For runnable snippets or manifest samples, prefer adding files under `examples/` and linking them from `README.md` if they are canonical demos.

## Scope of v0.1

AOS v0.1 is intentionally minimal.

The spec defines physical zones (Oracle / Permitted / Prohibited), hook-level interception requirements, separation between generation and evaluation, and evidence obligations.

Debates about general agent architecture, model choice, or non-filesystem tooling policies are **out of scope** for this repository unless they directly bear on §4 enforcement mechanics.

## Review expectations

- Prefer citations to stable section IDs (`§x.y`) when discussing the text.
- Keep examples vendor-neutral unless explicitly labeled as environment-specific reference wiring.

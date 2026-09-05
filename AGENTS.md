# AGENTS.md

## Run

```bash
python main.py
```

Run from repo root. Requires `matplotlib` (already in `venv/`).

## Project

Single-file Python project (`main.py`) that cracks a homophonic substitution cipher.

- `ciphertext.txt`: pipe-delimited ciphertext. Tokens separated by `|`. Non-homophone tokens (spaces, punctuation, numbers) break n-gram chains.
- Homophone tokens match pattern `[a-z][0-9]` (e.g., `b3`, `j6`).
- Currently counts homophone, bigram, and trigram frequencies. Mapping/decryption logic is not yet implemented.

## No tests or CI

There are no tests, linter, type checker, or CI config. If adding tests, keep them simple and runnable with `python -m pytest`.

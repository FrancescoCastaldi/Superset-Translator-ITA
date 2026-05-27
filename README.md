# Superset PO Translator

[![CI](https://github.com/FrancescoCastaldi/Superset-Translator-ITA/actions/workflows/ci.yml/badge.svg)](https://github.com/FrancescoCastaldi/Superset-Translator-ITA/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/FrancescoCastaldi/Superset-Translator-ITA/graph/badge.svg)](https://codecov.io/gh/FrancescoCastaldi/Superset-Translator-ITA)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff--format-orange)](https://github.com/astral-sh/ruff)

Automated English → Italian translator for Apache Superset `.po` translation files.  
Uses the Google Translate free API, protects technical terms from being altered, and removes `fuzzy` flags automatically.

---

## Features

- Translates all untranslated and `fuzzy`-flagged entries
- Protects technical terms (API, SQL, JWT, OAuth, …) from mistranslation
- Handles both singular and plural PO forms
- Rate-limited requests to avoid Google Translate throttling
- Clean CLI with configurable input/output paths

---

## Project Structure

```
superset-po-translator/
├── src/
│   └── translator/
│       ├── __init__.py       # Public API
│       ├── translator.py     # Core PO orchestration
│       ├── protection.py     # Technical term guard
│       └── google.py         # Google Translate client
├── tests/
│   ├── test_translator.py
│   ├── test_protection.py
│   └── test_google.py
├── scripts/
│   └── run.py                # CLI entry-point
├── .github/workflows/
│   └── ci.yml                # Lint + test + coverage
├── pyproject.toml            # Build, deps, tooling config
├── LICENSE
└── README.md
```

---

## Installation

```bash
git clone https://github.com/FrancescoCastaldi/Superset-Translator-ITA.git
cd Superset-Translator-ITA

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e .                   # install package
pip install -e ".[dev]"            # include dev tools (ruff, mypy, pytest)
```

---

## Usage

### Basic

```bash
# Translate messages.po → messages_it.po (defaults)
python scripts/run.py

# Custom input/output paths
python scripts/run.py path/to/input.po path/to/output_it.po
```

### With a fresh Superset clone

```bash
cp /path/to/superset/superset/translations/it/LC_MESSAGES/messages.po .
python scripts/run.py
```

### Expected output

```
Found 4523 entries in 'messages.po'
  ✓ 1/4523 - 'Add a filter'
  - 2/4523 - Already translated
  ✓ 3/4523 - 'Save dashboard'
    ↳ [singular] 'item' → 'elemento'
    ↳ [plural[1]] 'items' → 'elementi'
...
Saving to 'messages_it.po'...
Done!
```

---

## Development

```bash
# Run tests
pytest tests/ -v

# Lint & format
ruff format src tests scripts
ruff check src tests scripts

# Type check
mypy src/translator
```

---

## Architecture

| Module | Responsibility |
|---|---|
| `translator.py` | Orchestrates PO file I/O and entry iteration |
| `protection.py` | Placeholder substitution for technical terms |
| `google.py` | HTTP client for Google Translate free API |
| `scripts/run.py` | CLI entry-point, argument parsing |

---

## Limitations

- Uses the **unofficial** Google Translate endpoint (`gtx`) — no API key needed but may be rate-limited on large files (>10k strings)
- Machine translations should be reviewed before merging into production
- Sleep interval of 0.1 s per request; full Superset translation file (~4500 strings) takes ~10 minutes

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes following [Conventional Commits](https://www.conventionalcommits.org/)
4. Push and open a Pull Request against `main`

---

## Author

**Francesco Castaldi**  
Software Engineer | Healthcare Business Consultant  
[LinkedIn](https://linkedin.com/in/francescocastaldi) · [GitHub](https://github.com/FrancescoCastaldi)

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

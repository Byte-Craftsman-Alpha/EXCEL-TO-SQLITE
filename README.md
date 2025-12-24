# SQL Explorer (Excel to SQL via Streamlit)

SQL Explorer lets you upload an Excel workbook and run ad-hoc SQL queries against its sheets (loaded into an in-memory SQLite DB) using a Streamlit web UI.

## Features
- Upload `.xlsx` / `.xls` files
- Converts sheets to SQLite tables (sheet names used as table names)
- Run arbitrary SQL queries and view results
- Inspect table schemas in the sidebar

## Requirements
- Python 3.8+
- See `requirements.txt` for needed Python packages.

## Quickstart
1. Create and (optionally) activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Open the URL printed by Streamlit (usually http://localhost:8501).

## Notes
- For `.xlsx` files the app uses `openpyxl` via pandas. For older `.xls` files `xlrd` is used.
- Column names are normalized by trimming and replacing spaces with underscores.
- The app uses an in-memory SQLite database; nothing is written to disk.

## Files added for GitHub
- `requirements.txt` — Python dependencies
- `.gitignore` — ignores virtual envs, caches and editor files
- `LICENSE` — MIT license
- `CONTRIBUTING.md` — contribution guidelines
- `CODE_OF_CONDUCT.md` — contribution conduct
- `.github/workflows/python-app.yml` — basic CI checks
- `docs/USAGE.md` — extended usage notes

## License
This project is released under the MIT License — see `LICENSE`.

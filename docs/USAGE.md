# Usage notes

- Upload an `.xlsx` or `.xls` workbook via the left sidebar.
- The first sheet will be suggested in the SQL query placeholder.
- Columns are normalized by trimming and replacing spaces with underscores.
- Large Excel files may consume significant memory since the app uses an in-memory SQLite DB.

Tips:
- Remove unnecessary columns or split large files to keep memory usage reasonable.
- If you see errors reading an `.xls` file, ensure `xlrd` is installed and the file format is supported.

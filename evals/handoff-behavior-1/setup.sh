#!/usr/bin/env bash
set -euo pipefail
git init -q -b main
git config user.email eval@example.com && git config user.name eval
cat > budget.py <<'PY'
def total(rows):
    return sum(r["amount"] for r in rows)
PY
git add . && git commit -qm "Add budget totals"
git switch -qc feat/csv-export
cat > export.py <<'PY'
import csv

def export(rows, path):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "amount", "note"])
        writer.writeheader()
        writer.writerows(rows)
PY
git add export.py && git commit -qm "Add CSV export"
printf '\n# TODO: encoding="utf-8"\n' >> export.py
cat > test_export.py <<'PY'
from export import export

def test_export_handles_unicode(tmp_path):
    export([{"date": "2026-01-01", "amount": 5, "note": "café"}], tmp_path / "out.csv")
PY

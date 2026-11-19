#!/usr/bin/env bash
set -euo pipefail
git init -q -b main
git config user.email eval@example.com && git config user.name eval
mkdir -p site
cat > site/index.html <<'H'
<html><body><h1>Acme Budget</h1><p>Track spending.</p></body></html>
H
cat > export.py <<'PY'
import csv

def export(rows, path):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "amount", "note"])
        writer.writeheader()
        writer.writerows(rows)
PY
git add . && git commit -qm "Add CSV export and landing page"
git switch -qc feat/csv-unicode

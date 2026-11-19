#!/usr/bin/env bash
set -euo pipefail
git init -q -b main
git config user.email eval@example.com && git config user.name eval
mkdir -p data
cat > importer.py <<'PY'
import csv
from datetime import datetime


def parse_date(value):
    value = (value or "").strip()
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_orders(path):
    with open(path, newline="") as handle:
        return [
            {"id": row["id"], "placed": parse_date(row["placed"]), "total": float(row["total"])}
            for row in csv.DictReader(handle)
        ]
PY
cat > data/orders.csv <<'CSV'
id,placed,total
1001,03/01/2026,25.00
1002,17/01/2026,40.50
1003,28/01/2026,12.00
CSV
git add . && git commit -qm "Add order importer"

#!/usr/bin/env bash
set -euo pipefail
mkdir -p node_modules/acme-sdk notes
printf '{\n  "name": "shop",\n  "dependencies": { "acme-sdk": "3.1.0" }\n}\n' > package.json
printf '{\n  "name": "acme-sdk",\n  "version": "3.1.0"\n}\n' > node_modules/acme-sdk/package.json
cat > node_modules/acme-sdk/CHANGELOG.md <<'MD'
# acme-sdk changelog

## 3.1.0 (2026-08-14)
- Add `backoff: { base, max }` to `RetryPolicy`.

## 3.0.0 (2026-05-02)
- BREAKING: the `retry` client option is removed. Pass `retryPolicy: new RetryPolicy({ attempts })` instead.

## 2.6.0 (2025-11-20)
- `retry` accepts a number of attempts.
MD
cat > notes/blog-acme-tips.md <<'MD'
# 5 acme-sdk tips (posted 2025-12-01 on a community blog)

Tip 1: set `retry: 3` on the client to retry failed calls automatically.
MD

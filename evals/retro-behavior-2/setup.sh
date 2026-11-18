#!/usr/bin/env bash
set -euo pipefail
cat > CLAUDE.md <<'MD'
# Project notes

- Package manager: pnpm. Use pnpm, never npm.
- Run tests with `pnpm test`.
MD
printf '{ "name": "app", "packageManager": "pnpm@9.12.0" }\n' > package.json

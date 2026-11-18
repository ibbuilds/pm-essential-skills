#!/usr/bin/env bash
set -euo pipefail
mkdir -p node_modules/fetchkit docs/fetchkit/v2 docs/fetchkit/v3
printf '{\n  "name": "app",\n  "dependencies": { "fetchkit": "^2.4.0" }\n}\n' > package.json
printf '{\n  "name": "fetchkit",\n  "version": "2.4.1"\n}\n' > node_modules/fetchkit/package.json
printf '# fetchkit v2 options\n\n- `timeoutMs` (number): abort the request after this many milliseconds.\n' > docs/fetchkit/v2/options.md
printf '# fetchkit v3 options (latest)\n\n- `timeout` (string): duration such as "5s". Replaces `timeoutMs`, which was removed in 3.0.\n' > docs/fetchkit/v3/options.md

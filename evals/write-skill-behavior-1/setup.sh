#!/usr/bin/env bash
set -euo pipefail
mkdir -p .claude-plugin skills evals
printf '{ "name": "team-skills" }\n' > .claude-plugin/plugin.json

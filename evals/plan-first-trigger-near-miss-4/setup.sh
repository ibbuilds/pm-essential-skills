#!/usr/bin/env bash
set -euo pipefail
cat > cleanup.py <<'P'
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Delete .tmp files in a folder")
    parser.add_argument("folder")
    args = parser.parse_args()
    for name in os.listdir(args.folder):
        if name.endswith(".tmp"):
            os.remove(os.path.join(args.folder, name))
            print(f"deleted {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
P

#!/usr/bin/env python3
"""Local deterministic payload experiment; byte/character counts, never token claims."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).resolve().parents[2] / 'skills/ibbuilds-pm-source-selection/scripts/capture_command.py'
CASES = {
    'short': "print('ok')",
    'repeated': "import os; os.write(1,b'row: unchanged\\n'*100000); os.write(2,b'notice\\n'*10000)",
    'hidden_failure': "import os; os.write(1,b'a'*100000+b'FAILURE'+b'z'*100000); raise SystemExit(7)",
}


def main():
    # A fixed prefix and fixed-length random suffix keep envelope sizes comparable.
    with tempfile.TemporaryDirectory(prefix='capture-measure-') as directory:
        for name, command in CASES.items():
            result = subprocess.run([sys.executable, str(SCRIPT), '--output-dir', directory,
                                     '--preview-bytes', '128', '--', sys.executable, '-c', command],
                                    capture_output=True, text=True)
            report = json.loads(result.stdout)
            print(json.dumps({
                'case': name, 'raw_bytes': sum(report[s]['bytes'] for s in ('stdout', 'stderr')),
                'preview_bytes': sum(report[s]['preview_bytes'] for s in ('stdout', 'stderr')),
                'delivered_json_bytes': len(result.stdout.encode('utf-8')),
                'delivered_json_characters': len(result.stdout),
                'producer_exit': report['exit_code'], 'wrapper_exit': result.returncode,
                'failure_in_preview': 'FAILURE' in report['stdout']['head'] + report['stdout']['tail'],
            }, sort_keys=True))


if __name__ == '__main__':
    main()

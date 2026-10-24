#!/usr/bin/env python3
"""Run an already-authorized foreground argv once; retain raw output and preview it.

Not a sandbox, redactor, timeout manager, or semantic success detector.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


MAX_PREVIEW_BYTES = 65536


def stream_summary(path, budget):
    """Hash in bounded chunks; preview at most budget raw bytes, head then tail."""
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while chunk := stream.read(65536):
            digest.update(chunk)
            size += len(chunk)
        stream.seek(0)
        head_size = min(size, (budget + 1) // 2 if size > budget else budget)
        head = stream.read(head_size)
        tail_size = min(size - head_size, budget - head_size)
        if tail_size:
            stream.seek(size - tail_size)
        tail = stream.read(tail_size)
    return {
        'path': str(path), 'bytes': size, 'sha256': digest.hexdigest(),
        'truncated': size > budget,
        'preview_bytes': len(head) + len(tail),
        'head': head.decode('utf-8', errors='replace'),
        'tail': tail.decode('utf-8', errors='replace'),
    }


def capture(argv, output_dir, preview_bytes):
    """Return a report and wrapper exit code; never retry a producer."""
    if not argv or not 0 <= preview_bytes <= MAX_PREVIEW_BYTES:
        raise ValueError('command required; preview bytes must be between 0 and 65536')
    output_path = Path(output_dir)
    try:
        root = output_path.resolve(strict=True)
    except RuntimeError as exc:
        # Python <=3.12 reports a symlink loop as RuntimeError, not OSError.
        raise ValueError(str(exc)) from exc
    run_dir = Path(tempfile.mkdtemp(prefix='capture-', dir=root))
    report = {'status': 'capture_error', 'exit_code': None,
              'artifact_dir': str(run_dir)}
    exit_code = 2
    try:
        with (run_dir / 'stdout.bin').open('xb') as stdout, (run_dir / 'stderr.bin').open('xb') as stderr:
            try:
                result = subprocess.run(argv, stdout=stdout, stderr=stderr, shell=False)
            except (OSError, ValueError) as exc:
                report.update(status='launch_error', error=str(exc))
            else:
                report.update(status='completed', exit_code=result.returncode)
                exit_code = result.returncode if result.returncode >= 0 else 128 - result.returncode
        for name in ('stdout', 'stderr'):
            report[name] = stream_summary(run_dir / (name + '.bin'), preview_bytes)
        (run_dir / 'summary.json').write_text(json.dumps(report, ensure_ascii=True) + '\n', encoding='utf-8')
    except OSError as exc:
        report.update(status='capture_error', error=str(exc))
        # A failed producer remains failed even when its capture cannot be inspected.
        if exit_code == 0:
            exit_code = 2
    return report, exit_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, help='existing task-scoped directory')
    parser.add_argument('--preview-bytes', type=int, default=1024, help='raw byte budget per stream (0..65536)')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='-- executable arg ...')
    args = parser.parse_args()
    argv = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        report, code = capture(argv, args.output_dir, args.preview_bytes)
    except (OSError, ValueError) as exc:
        report, code = {'status': 'capture_error', 'exit_code': None, 'error': str(exc)}, 2
    utf8_stdout = (sys.stdout.encoding or "ascii").lower().replace("-", "").replace("_", "") == "utf8"
    payload = json.dumps(report, ensure_ascii=not utf8_stdout, separators=(',', ':'))
    # POSIX paths can contain surrogateescaped bytes even with UTF-8 stdout.
    if utf8_stdout:
        payload = payload.encode('utf-8', errors='backslashreplace').decode('utf-8')
    print(payload)
    return code


if __name__ == '__main__':
    sys.exit(main())

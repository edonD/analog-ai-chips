#!/usr/bin/env python3
"""
evaluate.py — Block 08: Mode Control pass/fail evaluator.
Reads specs.tsc and run.log from the current directory.
Prints a formatted summary and exits 0 if all specs pass, 1 otherwise.

Usage:
    cd 00_error_amp
    python3 evaluate.py

Expected: run.log exists and contains lines like:
    phase_margin: 67.3
    dc_gain: 72.1
    ...
"""

import sys
import os


def read_specs(path):
    metrics = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 6 or parts[0] == 'metric':
                continue
            metrics.append({
                'name': parts[0],
                'pattern': parts[1].lstrip('^'),
                'operator': parts[2],
                'threshold': float(parts[3]),
                'unit': parts[4],
                'primary': parts[5].strip().lower() == 'yes',
            })
    return metrics


def read_log(path):
    try:
        with open(path) as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def extract_value(lines, pattern):
    """Find the last line starting with pattern and return the numeric value."""
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.startswith(pattern):
            after = stripped[len(pattern):]
            after = after.lstrip(':').strip()
            try:
                return float(after.split()[0])
            except (ValueError, IndexError):
                pass
    return None


def check(value, operator, threshold):
    if operator == '>=':
        return value >= threshold
    elif operator == '<=':
        return value <= threshold
    elif operator == '==':
        return abs(value - threshold) < 1e-9
    return False


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    specs_path = 'specs.tsc'
    log_path = 'run.log'

    if not os.path.exists(specs_path):
        print(f'ERROR: {specs_path} not found', file=sys.stderr)
        sys.exit(2)

    metrics = read_specs(specs_path)
    if not metrics:
        print('ERROR: no metrics in specs.tsc', file=sys.stderr)
        sys.exit(2)

    log_lines = read_log(log_path)
    if not log_lines:
        print(f'WARNING: {log_path} empty or missing — no simulation results', file=sys.stderr)

    results = []
    n_pass = 0
    n_fail = 0
    n_missing = 0
    primary_name = None
    primary_value = None

    for m in metrics:
        value = extract_value(log_lines, m['pattern'])
        if value is None:
            status = 'MISSING'
            n_missing += 1
        elif check(value, m['operator'], m['threshold']):
            status = 'PASS'
            n_pass += 1
        else:
            status = 'FAIL'
            n_fail += 1

        results.append((m['name'], value, m['operator'], m['threshold'], m['unit'], status, m['primary']))
        if m['primary']:
            primary_name = m['name']
            primary_value = value

    n_total = len(metrics)
    print('---')
    for name, value, op, thresh, unit, status, is_primary in results:
        val_str = f'{value:.4g}' if value is not None else '???'
        marker = '*' if is_primary else ' '
        print(f'{marker} {name:<32s} {val_str:>10s}  {unit:<8s}  (spec {op} {thresh})  {status}')

    print(f'specs_pass: {n_pass}/{n_total}')
    if primary_name and primary_value is not None:
        print(f'primary ({primary_name}): {primary_value:.6g}')

    sys.exit(0 if (n_fail == 0 and n_missing == 0) else 1)


if __name__ == '__main__':
    main()

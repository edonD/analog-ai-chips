#!/usr/bin/env python3
"""VibroSense-1 Full-Chain Simulation Orchestrator.

Usage:
    python run_fullchain.py --classifier-test   # Quick classifier validation
    python run_fullchain.py --assemble          # Prepare netlists for each test case
    python run_fullchain.py --simulate normal   # Run one test case
    python run_fullchain.py --simulate all      # Run all 4 test cases
    python run_fullchain.py --check             # Parse results, check pass/fail
"""

import os
import sys
import subprocess
import argparse
import json
import time
import re

BASE = os.path.dirname(os.path.abspath(__file__))
FULLCHAIN = os.path.dirname(BASE)
VIBROSENSE = os.path.dirname(FULLCHAIN)

NETLISTS = os.path.join(FULLCHAIN, 'netlists')
STIMULI = os.path.join(FULLCHAIN, 'stimuli')
RESULTS = os.path.join(FULLCHAIN, 'results')
SCRIPTS = BASE

# Test cases
TEST_CASES = ['normal', 'inner_race', 'outer_race', 'ball']
EXPECTED_CLASS = {'normal': 0, 'inner_race': 1, 'ball': 2, 'outer_race': 3}
CLASS_VOLTAGE = {0: 0.0, 1: 0.45, 2: 0.9, 3: 1.35}


def run_ngspice(spice_file, log_file=None, raw_file=None):
    """Run ngspice in batch mode."""
    cmd = ['ngspice', '-b']
    if log_file:
        cmd += ['-o', log_file]
    if raw_file:
        cmd += ['-r', raw_file]
    cmd.append(spice_file)

    print(f"  Running: {' '.join(cmd)}")
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    elapsed = time.time() - t0
    print(f"  Completed in {elapsed:.1f}s (exit code {result.returncode})")

    if result.returncode != 0:
        print(f"  STDERR: {result.stderr[:500]}")
        if log_file and os.path.exists(log_file):
            with open(log_file) as f:
                content = f.read()
            # Check for convergence errors
            if 'singular matrix' in content.lower() or 'no convergence' in content.lower():
                print("  WARNING: Convergence issues detected")

    return result.returncode, elapsed


def run_classifier_test():
    """Quick classifier validation with feature vectors."""
    print("=" * 60)
    print("CLASSIFIER-ONLY TEST (feature vectors)")
    print("=" * 60)

    spice = os.path.join(NETLISTS, 'tb_classifier_vectors.spice')
    log = os.path.join(RESULTS, 'classifier_vectors.log')
    raw = os.path.join(RESULTS, 'classifier_vectors.raw')

    os.makedirs(RESULTS, exist_ok=True)
    rc, elapsed = run_ngspice(spice, log, raw)

    if rc != 0:
        print("FAIL: ngspice returned non-zero exit code")
        return False

    # Parse measurements from log
    if os.path.exists(log):
        with open(log) as f:
            log_content = f.read()

        # Expected: vectors 0-4=class0(0V), 5-9=class1(0.45V),
        #           10-14=class2(0.9V), 15-19=class3(1.35V)
        expected = [0]*5 + [1]*5 + [2]*5 + [3]*5
        correct = 0
        total = 0
        results = []

        for i in range(20):
            pattern = rf'class_v{i}\s*=\s*([-\d.eE+]+)'
            m = re.search(pattern, log_content)
            if m:
                voltage = float(m.group(1))
                # Decode class from voltage
                if voltage < 0.225:
                    detected = 0
                elif voltage < 0.675:
                    detected = 1
                elif voltage < 1.125:
                    detected = 2
                else:
                    detected = 3

                exp = expected[i]
                match = detected == exp
                if match:
                    correct += 1
                total += 1
                results.append((i, exp, detected, voltage, match))

        print(f"\nClassifier Results: {correct}/{total} correct "
              f"({100*correct/total:.1f}%)" if total > 0 else "No results parsed")

        class_names = ['Normal', 'Inner Race', 'Ball', 'Outer Race']
        for i, exp, det, v, match in results:
            status = "OK" if match else "MISMATCH"
            print(f"  Vec {i:2d}: expected={class_names[exp]}, "
                  f"got={class_names[det]} (V={v:.3f}) [{status}]")

        # Save results
        result_dict = {
            'total_vectors': total,
            'correct': correct,
            'accuracy': correct/total if total > 0 else 0,
            'details': [{'vector': i, 'expected': exp, 'detected': det,
                         'voltage': v, 'match': match}
                        for i, exp, det, v, match in results]
        }
        with open(os.path.join(RESULTS, 'classifier_test_results.json'), 'w') as f:
            json.dump(result_dict, f, indent=2)

        return correct == total if total > 0 else False
    return False


def assemble_test_netlist(test_case):
    """Create a test-specific netlist that includes the stimulus file."""
    top_spice = os.path.join(NETLISTS, 'vibrosense1_top.spice')
    stim_file = os.path.join(STIMULI, f'{test_case}_stimulus.pwl')
    out_spice = os.path.join(NETLISTS, f'vibrosense1_{test_case}.spice')

    if not os.path.exists(stim_file):
        print(f"ERROR: Stimulus file missing: {stim_file}")
        print("Run: python scripts/generate_stimuli.py first")
        return None

    # Read top-level netlist
    with open(top_spice) as f:
        content = f.read()

    # Replace default Vin with stimulus include
    # Remove the placeholder Vin line
    content = content.replace(
        'Vin vin gnd SIN(0.9 0.05 1000 0 0 0)',
        f'* Stimulus for test case: {test_case}\n'
        f'.include ../../10_fullchain/stimuli/{test_case}_stimulus.pwl'
    )

    # No simulation time adjustment needed — top.spice already has correct .tran

    with open(out_spice, 'w') as f:
        f.write(content)

    print(f"  Assembled: {out_spice}")
    return out_spice


def simulate_test_case(test_case):
    """Run simulation for one test case."""
    print(f"\n{'='*60}")
    print(f"SIMULATING: {test_case}")
    print(f"{'='*60}")

    netlist = assemble_test_netlist(test_case)
    if netlist is None:
        return False

    log = os.path.join(RESULTS, f'fullchain_{test_case}.log')
    raw = os.path.join(RESULTS, f'fullchain_{test_case}.raw')

    rc, elapsed = run_ngspice(netlist, log, raw)

    result = {
        'test_case': test_case,
        'exit_code': rc,
        'elapsed_seconds': elapsed,
        'log_file': log,
        'raw_file': raw,
        'success': rc == 0
    }

    with open(os.path.join(RESULTS, f'sim_status_{test_case}.json'), 'w') as f:
        json.dump(result, f, indent=2)

    return rc == 0


def check_results():
    """Parse all simulation results and generate summary."""
    print(f"\n{'='*60}")
    print("RESULTS CHECK")
    print(f"{'='*60}")

    summary = {}

    # Check classifier test
    clf_results = os.path.join(RESULTS, 'classifier_test_results.json')
    if os.path.exists(clf_results):
        with open(clf_results) as f:
            clf = json.load(f)
        summary['classifier_test'] = clf
        print(f"\nClassifier-only test: {clf['correct']}/{clf['total_vectors']} "
              f"({clf['accuracy']*100:.1f}%)")
    else:
        print("\nClassifier-only test: NOT RUN")

    # Check full-chain results
    for tc in TEST_CASES:
        status_file = os.path.join(RESULTS, f'sim_status_{tc}.json')
        if os.path.exists(status_file):
            with open(status_file) as f:
                status = json.load(f)
            print(f"\n{tc}: {'PASS' if status['success'] else 'FAIL'} "
                  f"({status['elapsed_seconds']:.1f}s)")
            summary[tc] = status
        else:
            print(f"\n{tc}: NOT RUN")

    # Write summary
    with open(os.path.join(RESULTS, 'simulation_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    return summary


def main():
    parser = argparse.ArgumentParser(description='VibroSense-1 Full-Chain Simulation')
    parser.add_argument('--classifier-test', action='store_true',
                        help='Run classifier-only test with feature vectors')
    parser.add_argument('--assemble', action='store_true',
                        help='Assemble test-specific netlists')
    parser.add_argument('--simulate', type=str, default=None,
                        help='Run simulation (normal/inner_race/outer_race/ball/all)')
    parser.add_argument('--check', action='store_true',
                        help='Parse results and check pass/fail')
    args = parser.parse_args()

    os.makedirs(RESULTS, exist_ok=True)

    if args.classifier_test:
        run_classifier_test()

    elif args.assemble:
        for tc in TEST_CASES:
            assemble_test_netlist(tc)

    elif args.simulate:
        if args.simulate == 'all':
            for tc in TEST_CASES:
                simulate_test_case(tc)
        elif args.simulate in TEST_CASES:
            simulate_test_case(args.simulate)
        else:
            print(f"Unknown test case: {args.simulate}")
            print(f"Valid: {TEST_CASES} or 'all'")
            sys.exit(1)

    elif args.check:
        check_results()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()

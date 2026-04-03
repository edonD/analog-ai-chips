#!/usr/bin/env python3
"""Download CWRU Bearing Dataset .mat files (12kHz drive-end).

Source: Case Western Reserve University Bearing Data Center
https://engineering.case.edu/bearingdatacenter

Downloads only the 12kHz drive-end accelerometer data for all motor loads
(0-3 HP) across normal + 3 fault types x 3 fault sizes.
"""

import os
import urllib.request
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# CWRU file numbers -> (filename, label, description)
# 12kHz drive-end data, all motor loads (0, 1, 2, 3 HP)
CWRU_FILES = {
    # Normal baseline
    '97':  ('normal_0hp_97.mat',  0, 'Normal 0HP'),
    '98':  ('normal_1hp_98.mat',  0, 'Normal 1HP'),
    '99':  ('normal_2hp_99.mat',  0, 'Normal 2HP'),
    '100': ('normal_3hp_100.mat', 0, 'Normal 3HP'),

    # Inner race fault — 0.007 inch
    '105': ('IR007_0hp_105.mat', 1, 'Inner Race 0.007" 0HP'),
    '106': ('IR007_1hp_106.mat', 1, 'Inner Race 0.007" 1HP'),
    '107': ('IR007_2hp_107.mat', 1, 'Inner Race 0.007" 2HP'),
    '108': ('IR007_3hp_108.mat', 1, 'Inner Race 0.007" 3HP'),
    # Inner race fault — 0.014 inch
    '169': ('IR014_0hp_169.mat', 1, 'Inner Race 0.014" 0HP'),
    '170': ('IR014_1hp_170.mat', 1, 'Inner Race 0.014" 1HP'),
    '171': ('IR014_2hp_171.mat', 1, 'Inner Race 0.014" 2HP'),
    '172': ('IR014_3hp_172.mat', 1, 'Inner Race 0.014" 3HP'),
    # Inner race fault — 0.021 inch
    '209': ('IR021_0hp_209.mat', 1, 'Inner Race 0.021" 0HP'),
    '210': ('IR021_1hp_210.mat', 1, 'Inner Race 0.021" 1HP'),
    '211': ('IR021_2hp_211.mat', 1, 'Inner Race 0.021" 2HP'),
    '212': ('IR021_3hp_212.mat', 1, 'Inner Race 0.021" 3HP'),

    # Ball fault — 0.007 inch
    '118': ('B007_0hp_118.mat', 2, 'Ball 0.007" 0HP'),
    '119': ('B007_1hp_119.mat', 2, 'Ball 0.007" 1HP'),
    '120': ('B007_2hp_120.mat', 2, 'Ball 0.007" 2HP'),
    '121': ('B007_3hp_121.mat', 2, 'Ball 0.007" 3HP'),
    # Ball fault — 0.014 inch
    '185': ('B014_0hp_185.mat', 2, 'Ball 0.014" 0HP'),
    '186': ('B014_1hp_186.mat', 2, 'Ball 0.014" 1HP'),
    '187': ('B014_2hp_187.mat', 2, 'Ball 0.014" 2HP'),
    '188': ('B014_3hp_188.mat', 2, 'Ball 0.014" 3HP'),
    # Ball fault — 0.021 inch
    '222': ('B021_0hp_222.mat', 2, 'Ball 0.021" 0HP'),
    '223': ('B021_1hp_223.mat', 2, 'Ball 0.021" 1HP'),
    '224': ('B021_2hp_224.mat', 2, 'Ball 0.021" 2HP'),
    '225': ('B021_3hp_225.mat', 2, 'Ball 0.021" 3HP'),

    # Outer race fault — 0.007 inch (centered @6:00)
    '130': ('OR007_6_0hp_130.mat', 3, 'Outer Race 0.007" @6 0HP'),
    '131': ('OR007_6_1hp_131.mat', 3, 'Outer Race 0.007" @6 1HP'),
    '132': ('OR007_6_2hp_132.mat', 3, 'Outer Race 0.007" @6 2HP'),
    '133': ('OR007_6_3hp_133.mat', 3, 'Outer Race 0.007" @6 3HP'),
    # Outer race fault — 0.014 inch
    '197': ('OR014_6_0hp_197.mat', 3, 'Outer Race 0.014" @6 0HP'),
    '198': ('OR014_6_1hp_198.mat', 3, 'Outer Race 0.014" @6 1HP'),
    '199': ('OR014_6_2hp_199.mat', 3, 'Outer Race 0.014" @6 2HP'),
    '200': ('OR014_6_3hp_200.mat', 3, 'Outer Race 0.014" @6 3HP'),
    # Outer race fault — 0.021 inch
    '234': ('OR021_6_0hp_234.mat', 3, 'Outer Race 0.021" @6 0HP'),
    '235': ('OR021_6_1hp_235.mat', 3, 'Outer Race 0.021" @6 1HP'),
    '236': ('OR021_6_2hp_236.mat', 3, 'Outer Race 0.021" @6 2HP'),
    '237': ('OR021_6_3hp_237.mat', 3, 'Outer Race 0.021" @6 3HP'),
}

BASE_URL = 'https://engineering.case.edu/sites/default/files/'


def download_cwru(data_dir=DATA_DIR):
    os.makedirs(data_dir, exist_ok=True)

    n_total = len(CWRU_FILES)
    n_done = 0
    n_skip = 0
    n_fail = 0

    for file_num, (fname, label, desc) in sorted(CWRU_FILES.items(), key=lambda x: x[0]):
        dest = os.path.join(data_dir, fname)
        if os.path.exists(dest):
            n_skip += 1
            n_done += 1
            continue

        url = f'{BASE_URL}{file_num}.mat'
        print(f'  [{n_done+1}/{n_total}] {desc} -> {fname} ...', end=' ', flush=True)
        try:
            urllib.request.urlretrieve(url, dest)
            size_kb = os.path.getsize(dest) / 1024
            print(f'{size_kb:.0f} KB')
            n_done += 1
        except Exception as e:
            print(f'FAILED: {e}')
            n_fail += 1
            if os.path.exists(dest):
                os.remove(dest)

    print(f'\nDone: {n_done - n_skip} downloaded, {n_skip} already existed, {n_fail} failed')
    return n_fail == 0


if __name__ == '__main__':
    print('Downloading CWRU Bearing Dataset (12kHz drive-end)...\n')
    ok = download_cwru()
    sys.exit(0 if ok else 1)

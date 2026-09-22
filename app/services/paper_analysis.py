"""Validate measured JMH CSV output without inventing benchmark results."""
import csv
import hashlib
import io
import math
import statistics
from collections import defaultdict


def analyze_csv(raw: bytes) -> dict:
    if not raw or len(raw) > 10 * 1024 * 1024:
        raise ValueError('Upload a nonempty CSV no larger than 10 MiB')
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    required = {'Benchmark', 'Mode', 'Score', 'Unit', 'Param: size', 'Param: seed', 'Param: distribution'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Required JMH columns: ' + ', '.join(sorted(required)))
    groups = defaultdict(list)
    cells = set()
    algorithms, distributions, sizes, seeds = set(), set(), set(), set()
    mode_units = set()
    for line, row in enumerate(reader, 2):
        algorithm = row.get('Param: algorithm') or row['Benchmark']
        distribution = row['Param: distribution']
        size, seed = int(row['Param: size']), int(row['Param: seed'])
        score = float(row['Score'])
        mode, unit = row['Mode'], row['Unit']
        if not algorithm.strip() or not distribution.strip() or size <= 0 or not math.isfinite(score) or score < 0:
            raise ValueError(f'Invalid benchmark values on line {line}')
        if mode not in {'avgt', 'sample', 'ss', 'thrpt'} or not unit.strip():
            raise ValueError(f'Invalid mode/unit on line {line}')
        key = (algorithm, distribution, size, seed)
        if key in cells:
            raise ValueError(f'Duplicate algorithm/distribution/size/seed on line {line}')
        cells.add(key)
        algorithms.add(algorithm); distributions.add(distribution); sizes.add(size); seeds.add(seed)
        mode_units.add((mode, unit))
        groups[(algorithm, distribution, size, mode, unit)].append(score)
    if not cells:
        raise ValueError('CSV contains no measured rows')
    if len(mode_units) != 1:
        raise ValueError('Analyze one JMH mode and unit at a time; mixed units cannot be compared')
    expected = len(algorithms) * len(distributions) * len(sizes) * len(seeds)
    summary = []
    for (algorithm, distribution, size, mode, unit), values in sorted(groups.items()):
        summary.append(dict(algorithm=algorithm, distribution=distribution, size=size,
                            mode=mode, unit=unit, seeds=len(values), mean=statistics.mean(values),
                            median=statistics.median(values), minimum=min(values), maximum=max(values)))
    return dict(sha256=hashlib.sha256(raw).hexdigest(), rows=len(cells),
                observed_matrix_complete=len(cells) == expected, expected_observed_matrix_rows=expected,
                missing_observed_matrix_rows=expected-len(cells),
                matches_planned_dimensions=(len(algorithms), len(distributions), len(sizes), len(seeds)) == (6,15,5,30),
                algorithms=sorted(algorithms), distributions=sorted(distributions), sizes=sorted(sizes),
                seeds=sorted(seeds), summary=summary,
                interpretation='Descriptive analysis of supplied measurements. Completeness does not validate experiment methodology or prove speedup.')

import csv, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from collections import Counter
d1 = list(csv.DictReader(open('data/tren_topik.csv', encoding='utf-8-sig')))
print('D1:', len(d1), '| sumber:', dict(Counter(r['sumber'] for r in d1)))
print()
for r in d1[-28:]:
    print(f"  [{r['sumber'][:38]}] {r['topik'][:75]}")

import csv, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
for name in ['data/tren_topik.csv']:
    rows = list(csv.DictReader(open(name, encoding='utf-8-sig')))
    print('=' * 20, name, len(rows))
    for r in rows:
        print(f"  [{r['kategori']}] {r.get('topik')}")

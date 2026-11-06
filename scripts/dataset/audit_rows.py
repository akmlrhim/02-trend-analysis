import csv, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
for name in ['data/tren_topik.csv', 'data/pertanyaan_audiens.csv']:
    rows = list(csv.DictReader(open(name, encoding='utf-8-sig')))
    print('=' * 20, name, len(rows))
    for r in rows:
        key = r.get('topik') or r.get('pertanyaan_atau_keluhan')
        print(f"  [{r['kategori']}] {key}")

import json, time
from pytrends.request import TrendReq

pyt = TrendReq(hl='id-ID', tz=420, timeout=(10, 50))
out = {}
seeds = ["belanja online", "resep masakan", "liburan", "smartphone", "skincare",
         "viral", "kripto", "lowongan kerja", "olahraga", "film indonesia"]

# Retry interest over time 30 hari (2 kata per payload biar ringan)
for name, kws in [("iot30a", seeds[:2]), ("iot30b", seeds[2:4]), ("iot30c", seeds[4:6]), ("iot30d", seeds[6:8]), ("iot30e", seeds[8:])]:
    try:
        pyt.build_payload(kws, timeframe='now 30-d', geo='ID')
        df = pyt.interest_over_time()
        out[name] = {c: {'avg': float(df[c].mean().round(1)), 'first': float(df[c].iloc[0]), 'last': float(df[c].iloc[-1]), 'max': float(df[c].max())} for c in df.columns if c != 'isPartial'}
    except Exception as e:
        out[name + '_error'] = repr(e)
    time.sleep(4)

# Related topics retry
rt = {}
for kw in seeds[:5]:
    try:
        pyt.build_payload([kw], timeframe='today 12-m', geo='ID')
        res = pyt.related_topics()
        d = res.get(kw)
        rows = {}
        for kind in ('rising', 'top'):
            if d and d.get(kind) is not None:
                rows[kind] = d[kind].head(8)[['value', 'topic_title', 'topic_type']].to_dict('records')
        rt[kw] = rows
    except Exception as e:
        rt[kw] = {'error': repr(e)}
    time.sleep(4)
out['related_topics'] = rt

with open('data/_pytrends_raw2.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("OK", list(out.keys()))

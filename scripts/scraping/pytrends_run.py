import json, sys, time
from pytrends.request import TrendReq

pyt = TrendReq(hl='id-ID', tz=420, timeout=(10, 50))
out = {}

seeds = ["belanja online", "resep masakan", "liburan", "smartphone", "skincare",
         "viral", "kripto", "lowongan kerja", "olahraga", "film indonesia"]

# Interest over time (12 bulan)
try:
    pyt.build_payload(seeds[:5], timeframe='today 12-m', geo='ID')
    iot12 = pyt.interest_over_time()
    out['iot12_1'] = {c: {'avg': float(iot12[c].mean().round(1)), 'first': float(iot12[c].iloc[0]), 'last': float(iot12[c].iloc[-1]), 'max': float(iot12[c].max())} for c in iot12.columns if c != 'isPartial'}
except Exception as e:
    out['iot12_1_error'] = repr(e)
time.sleep(3)
try:
    pyt.build_payload(seeds[5:], timeframe='today 12-m', geo='ID')
    iot12b = pyt.interest_over_time()
    out['iot12_2'] = {c: {'avg': float(iot12b[c].mean().round(1)), 'first': float(iot12b[c].iloc[0]), 'last': float(iot12b[c].iloc[-1]), 'max': float(iot12b[c].max())} for c in iot12b.columns if c != 'isPartial'}
except Exception as e:
    out['iot12_2_error'] = repr(e)
time.sleep(3)

# Interest over time 30 hari (2 batch)
try:
    pyt.build_payload(seeds[:5], timeframe='now 30-d', geo='ID')
    iot30 = pyt.interest_over_time()
    out['iot30_1'] = {c: {'avg': float(iot30[c].mean().round(1)), 'first': float(iot30[c].iloc[0]), 'last': float(iot30[c].iloc[-1]), 'max': float(iot30[c].max())} for c in iot30.columns if c != 'isPartial'}
except Exception as e:
    out['iot30_1_error'] = repr(e)
time.sleep(3)
try:
    pyt.build_payload(seeds[5:], timeframe='now 30-d', geo='ID')
    iot30b = pyt.interest_over_time()
    out['iot30_2'] = {c: {'avg': float(iot30b[c].mean().round(1)), 'first': float(iot30b[c].iloc[0]), 'last': float(iot30b[c].iloc[-1]), 'max': float(iot30b[c].max())} for c in iot30b.columns if c != 'isPartial'}
except Exception as e:
    out['iot30_2_error'] = repr(e)
time.sleep(3)

# Related queries + topics per keyword (2 batch x rising/top)
rq = {}
for kw in seeds:
    try:
        pyt.build_payload([kw], timeframe='today 12-m', geo='ID')
        res = pyt.related_queries()
        k = res.get(kw, {})
        rq[kw] = {
            'rising': k['rising'].head(10).to_dict('records') if k.get('rising') is not None else None,
            'top': k['top'].head(10).to_dict('records') if k.get('top') is not None else None,
        }
    except Exception as e:
        rq[kw] = {'error': repr(e)}
    time.sleep(2)
out['related_queries'] = rq

# Related topics
rt = {}
for kw in seeds[:5]:
    try:
        pyt.build_payload([kw], timeframe='today 12-m', geo='ID')
        res = pyt.related_topics()
        d = res.get(kw)
        if d and d.get('rising') is not None:
            rt[kw] = d['rising'].head(8)[['value', 'topic_title', 'topic_type']].to_dict('records')
    except Exception as e:
        rt[kw] = {'error': repr(e)}
    time.sleep(2)
out['related_topics'] = rt

# Interest by region
ibr = {}
for kw in seeds[:5]:
    try:
        pyt.build_payload([kw], timeframe='today 12-m', geo='ID')
        res = pyt.interest_by_region(resolution='PROVINCE', inc_low_vol=False)
        top = res[kw].sort_values(ascending=False).head(10)
        ibr[kw] = {str(k2): float(v) for k2, v in top.items()}
    except Exception as e:
        ibr[kw] = {'error': repr(e)}
    time.sleep(2)
out['interest_by_region'] = ibr

with open('data/_pytrends_raw.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("OK - sections:", list(out.keys()))

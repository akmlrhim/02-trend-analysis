# -*- coding: utf-8 -*-
"""Riset khusus tren Instagram: Google Trends ID, interest 12 bulan + rising queries.
Output: data/_instagram_trends_raw.json"""
import json, sys, time
from pytrends.request import TrendReq
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JEDA = 20   # jeda antar request, hindari 429
RETRY = 3   # coba ulang tiap request saat 429

pyt = TrendReq(hl="id-ID", tz=420, timeout=(10, 50))
out = {}


def dgn_retry(fn):
    for coba in range(RETRY):
        try:
            return fn()
        except Exception as e:
            if coba == RETRY - 1:
                raise
            print("  429, tunggu %d detik..." % (45 * (coba + 1)), flush=True)
            time.sleep(45 * (coba + 1))


seeds = ["instagram reels", "instagram story", "feed instagram", "konten instagram",
         "capcut template", "trending audio", "hashtag instagram", "instagram bio"]

# 1. Interest over time 12 bulan (2 batch per 4 kata agar payload aman)
for bi in range(0, len(seeds), 4):
    batch = seeds[bi:bi + 4]
    try:
        def iot():
            pyt.build_payload(batch, timeframe="today 12-m", geo="ID")
            df = pyt.interest_over_time()
            return {c: {"avg": float(df[c].mean().round(1)),
                        "first": float(df[c].iloc[0]),
                        "last": float(df[c].iloc[-1]),
                        "max": float(df[c].max())}
                    for c in df.columns if c != "isPartial"}
        out["iot12_%d" % bi] = dgn_retry(iot)
        print("  iot12 batch %d OK: %s" % (bi, list(out["iot12_%d" % bi].keys())), flush=True)
    except Exception as e:
        out["iot12_%d_error" % bi] = repr(e)
    time.sleep(JEDA)

# 2. Rising related queries per seed = sinyal "naik" paling akurat
rq = {}
for kw in seeds:
    try:
        def related():
            pyt.build_payload([kw], timeframe="today 12-m", geo="ID")
            res = pyt.related_queries()
            k = res.get(kw, {})
            rising = k.get("rising")
            top = k.get("top")
            return {
                "rising": rising.head(12).to_dict("records") if rising is not None else None,
                "top": top.head(8).to_dict("records") if top is not None else None,
            }
        rq[kw] = dgn_retry(related)
        n = len((rq[kw] or {}).get("rising") or [])
        print("  rising '%s': %d" % (kw, n), flush=True)
    except Exception as e:
        rq[kw] = {"error": repr(e)}
    time.sleep(JEDA)
out["related_queries"] = rq

# 3. Interest by region untuk 2 seed utama (siapa audiensnya, di mana)
ibr = {}
for kw in ["instagram reels", "konten instagram"]:
    try:
        def ibr1():
            pyt.build_payload([kw], timeframe="today 12-m", geo="ID")
            res = pyt.interest_by_region(resolution="PROVINCE", inc_low_vol=False)
            top = res[kw].sort_values(ascending=False).head(8)
            return {str(k2): float(v) for k2, v in top.items()}
        ibr[kw] = dgn_retry(ibr1)
    except Exception as e:
        ibr[kw] = {"error": repr(e)}
    time.sleep(JEDA)
out["interest_by_region"] = ibr

with open("data/_instagram_trends_raw.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

n_rising = sum(len(v.get("rising") or []) for v in rq.values() if isinstance(v, dict))
n_ok = sum(1 for k in out if k.startswith("iot12_") and not k.endswith("_error"))
print("OK - iot12: %d batch | rising total: %d" % (n_ok, n_rising))

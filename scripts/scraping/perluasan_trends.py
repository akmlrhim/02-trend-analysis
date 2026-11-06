# -*- coding: utf-8 -*-
"""Riset tren digital marketing luas: Google Trends ID untuk banyak tema.
Output: data/_perluasan_trends_raw.json"""
import json, sys, time
from pytrends.request import TrendReq
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JEDA = 15
RETRY = 2
pyt = TrendReq(hl="id-ID", tz=420, timeout=(10, 50))
out = {}

def dgn_retry(fn):
    for coba in range(RETRY):
        try:
            return fn()
        except Exception as e:
            if coba == RETRY - 1:
                raise
            print("  429, tunggu %d detik..." % (60 * (coba + 1)), flush=True)
            time.sleep(60 * (coba + 1))

seeds = ["tiktok shop", "live shopping", "whatsapp business", "google ads",
         "seo", "influencer", "marketplace", "umkm digital",
         "ai content", "email marketing", "website toko online", "jasa digital marketing"]

rq = {}
for kw in seeds:
    try:
        def related():
            pyt.build_payload([kw], timeframe="today 12-m", geo="ID")
            res = pyt.related_queries()
            k = res.get(kw, {})
            rising = k.get("rising")
            return rising.head(10).to_dict("records") if rising is not None else []
        rq[kw] = dgn_retry(related)
        print("  rising '%s': %d" % (kw, len(rq[kw])), flush=True)
    except Exception as e:
        rq[kw] = {"error": repr(e)}
    time.sleep(JEDA)
out["related_queries"] = rq

# interest 12 bulan per tema utama (batch 4-4-4)
for bi in range(0, len(seeds), 4):
    batch = seeds[bi:bi + 4]
    try:
        def iot():
            pyt.build_payload(batch, timeframe="today 12-m", geo="ID")
            df = pyt.interest_over_time()
            return {c: {"avg": float(df[c].mean().round(1)), "first": float(df[c].iloc[0]),
                        "last": float(df[c].iloc[-1])} for c in df.columns if c != "isPartial"}
        out["iot12_%d" % bi] = dgn_retry(iot)
        print("  iot12 batch %d OK" % bi, flush=True)
    except Exception as e:
        out["iot12_%d_error" % bi] = repr(e)
    time.sleep(JEDA)

with open("data/_perluasan_trends_raw.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("OK selesai")

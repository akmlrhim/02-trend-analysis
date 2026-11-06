# -*- coding: utf-8 -*-
"""Fallback scraping Python untuk sumber yang gagal lewat MCP/fetch: Reddit, YouTube trending, Trends 30 hari."""
import json, re, requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "id-ID,id;q=0.9"}
out = {}

# 1. Reddit r/indonesia hot/bulan ini (fallback: HTML old.reddit)
try:
    r = requests.get("https://old.reddit.com/r/indonesia/top/?sort=top&t=month", headers=UA, timeout=30)
    out["reddit_status"] = r.status_code
    if r.status_code == 200:
        rows = re.findall(r'<a class="title[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>[\s\S]{0,400}?(\d+) points?', r.text)
        # simpler: parse entries
        entries = re.findall(r'<div class=" top-matter">(.*?)</div>\s*</div>', r.text, re.S)
        posts = []
        for m in re.finditer(r'<a class="title may-blank[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', r.text):
            posts.append({"url": m.group(1), "title": m.group(2).strip()})
        scores = re.findall(r'<div class="score unvoted"[^>]*>([^<]+)</div>', r.text)
        for i, p in enumerate(posts[:40]):
            if i < len(scores):
                p["score"] = scores[i]
        out["reddit_posts"] = posts[:40]
except Exception as e:
    out["reddit_error"] = repr(e)

# 2. YouTube trending ID (fallback: ytInitialData)
try:
    s = requests.Session()
    s.cookies.set("CONSENT", "YES+cb.20240101-00-p0.en+FX+100", domain=".youtube.com")
    r = s.get("https://www.youtube.com/feed/trending?hl=id&gl=ID", headers=UA, timeout=30)
    out["yt_status"] = r.status_code
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]{15,120})"\}\]', r.text)
    out["yt_titles"] = list(dict.fromkeys(titles))[:30]
    if not out["yt_titles"]:
        t2 = re.findall(r'"videoId":"([^"]{11})"[\s\S]{0,400}?"title":\{"simpleText":"([^"]{10,120})"\}', r.text)
        out["yt_titles2"] = [{"id": a, "t": b} for a, b in t2[:30]]
except Exception as e:
    out["yt_error"] = repr(e)

# 3. Google Trends interest over time 30 hari (fallback: endpoint widget langsung)
try:
    s = requests.Session()
    s.headers.update(UA)
    # token umum untuk widget timeseries
    r0 = s.get("https://trends.google.com/trends/api/explore?hl=id-ID&tz=-420&req=%7B%22comparisonItem%22%3A%5B%7B%22keyword%22%3A%22skincare%22%2C%22geo%22%3A%22ID%22%2C%22time%22%3A%22now%207-d%22%7D%5D%2C%22category%22%3A0%2C%22property%22%3A%22%22%7D")
    body = r0.text.replace(")]}',", "")
    out["trends_explore_status"] = r0.status_code
    try:
        j = json.loads(body)
        widget = j["widgets"][0]
        tok = widget.get("token")
        rid = widget["request"]
        r1 = s.get("https://trends.google.com/trends/api/widgetdata/multiline/csv?hl=id-ID&tz=-420&token=" + tok + "&req=" + requests.utils.quote(json.dumps(rid)))
        out["trends_csv_status"] = r1.status_code
        out["trends_csv_head"] = r1.text[:1500] if r1.status_code == 200 else r1.text[:200]
    except Exception as e2:
        out["trends_parse_error"] = repr(e2) + " | body head: " + body[:300]
except Exception as e:
    out["trends_error"] = repr(e)

print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])

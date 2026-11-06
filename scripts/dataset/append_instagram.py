# -*- coding: utf-8 -*-
"""Masukkan hasil riset khusus Instagram ke data/tren_topik.csv.
Hanya tren dengan bukti kuantitatif (skor/volume) atau sumber kredibel.
Jalankan dari root: python scripts/dataset/append_instagram.py"""
import csv, json, sys
from datetime import date
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = date.today().isoformat()
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]

raw = json.load(open("data/_instagram_trends_raw.json", encoding="utf-8"))
baris = []

def add(topik, kata_kunci, sumber, indikator, skor, sentimen, url):
    baris.append(dict(zip(H1, (TGL, "media_sosial", topik, kata_kunci, sumber,
                               indikator, skor, sentimen, url))))

# 1. Rising queries Google Trends (bukti kuantitatif: % kenaikan)
RISING_URL = "https://trends.google.com/trends/explore?geo=ID"
for kw, d in raw.get("related_queries", {}).items():
    if not isinstance(d, dict) or d.get("error"):
        continue
    for r in (d.get("rising") or [])[:8]:
        q = r.get("query", "")
        g = r.get("growth", "")
        add("Instagram rising: %s (+%s)" % (q, g), kw,
            "Google Trends (Related Queries - Rising)", "naik", str(g).rstrip("%"),
            "netral", RISING_URL)
    for r in (d.get("top") or [])[:5]:
        q = r.get("query", "")
        v = r.get("value", "")
        add("Instagram populer: %s" % q, kw,
            "Google Trends (Related Queries - Top)", "stabil", str(v),
            "netral", RISING_URL)

# 2. Interest 12 bulan yang naik (last > first berarti naik riil, bukan sekadar viral sekejap)
for k, d in raw.items():
    if not k.startswith("iot12_") or k.endswith("_error"):
        continue
    for kw, m in d.items():
        if m["last"] > m["first"] * 1.15:  # naik >15% dibanding awal periode
            add("Interest 12 bulan: %s (%s -> %s)" % (kw, int(m["first"]), int(m["last"])),
                kw, "Google Trends (Interest Over Time)", "naik", str(m["avg"]), "netral", RISING_URL)

# 3. Hashtag Instagram terverifikasi (iqhashtags) - volume riil
add("Hashtag Instagram: #reelsindonesia (1.1M post/hari 844.6K)", "reelsindonesia; reelsinstagram",
    "Instagram Hashtag (agregator iqhashtags)", "naik", "844600", "netral",
    "https://iqhashtags.com/hashtags/hashtag/reelsindonesia")
add("Hashtag Instagram: #reelsinstagram (553.7M post, 247.6K/hari)", "reelsinstagram",
    "Instagram Hashtag (agregator iqhashtags)", "stabil", "247600", "netral",
    "https://iqhashtags.com/hashtags/hashtag/reelsindonesia")
add("Hashtag Instagram: #umkmindonesia (3.3M post, avg likes 4.3K)", "umkmindonesia; umkmnaikkelas",
    "Instagram Hashtag (agregator iqhashtags)", "stabil", "3300000", "positif",
    "https://iqhashtags.com/hashtags/hashtag/umkmindonesia")
add("Hashtag Instagram: #digitalmarketing (45.3M post, 12.2K/hari)", "digitalmarketing",
    "Instagram Hashtag (agregator iqhashtags)", "stabil", "12200", "netral",
    "https://iqhashtags.com/hashtags/hashtag/reelsindonesia")

# 4. Statistik algoritma/format dari sumber kredibel (bukan tren abal: angka resmi Meta/platform)
add("Algoritma Reels 2026: DM share (sends per reach) sinyal ranking terkuat untuk jangkauan non-follower",
    "sends per reach; dm share", "Statistik industri (vidico/hootsuite 2026)", "naik", "", "netral",
    "https://vidico.com/news/instagram-reels-statistics")
add("Reels di-share 4.5 miliar kali per hari; ranking Reels naik 10% waktu tontonan Q1 2026",
    "reels share; waktu tontonan", "Statistik industri (hootsuite/creatorflow 2026)", "naik", "4500000000", "netral",
    "https://blog.hootsuite.com/instagram-statistics")
add("Reels <90 detik dengan jump cut tiap 3-5 detik: engagement +32%, hook 3 detik pertama +72% peluang viral",
    "reels pendek; hook 3 detik", "Statistik industri (loopexdigital 2026)", "naik", "32", "netral",
    "https://www.loopexdigital.com/blog/instagram-reels-statistics")
add("Reels pakai trending audio: engagement +42%; reach rate rata-rata Reels 30.81%",
    "trending audio; reach reels", "Statistik industri (loopexdigital/demandsage 2026)", "naik", "42", "netral",
    "https://www.loopexdigital.com/blog/instagram-reels-statistics")

# Dedupe lalu tulis
rows = list(csv.DictReader(open("data/tren_topik.csv", encoding="utf-8-sig")))
ada = {"|".join(r[k].strip().lower() for k in ("kategori", "topik")) for r in rows}
n = 0
for b in baris:
    key = (b["kategori"] + "|" + b["topik"]).lower()
    if key not in ada:
        rows.append(b)
        ada.add(key)
        n += 1

with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1)
    w.writeheader()
    w.writerows(rows)

print(f"tren_topik.csv: +{n} baris Instagram baru (total {len(rows)})")

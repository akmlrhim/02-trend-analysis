# -*- coding: utf-8 -*-
"""Integrasi hasil perluasan Google Trends (12 tema) ke tren_topik.csv.
Rising queries dikelompokkan jadi judul narasi; query junk dibuang.
Jalankan dari root: python scripts/dataset/append_perluasan_trends.py"""
import csv, json, sys
from datetime import date
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = date.today().isoformat()
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
URL = "https://trends.google.com/trends/explore?geo=ID"

raw = json.load(open("data/_perluasan_trends_raw.json", encoding="utf-8"))

# kumpulkan semua rising query per tema (buang junk)
JUNK = ("png", "netflix", "siapa", "concert", "fruit", "meditation", "lidl", "near me",
        "password", "signature", "verify", "how to transfer", "født", "actor", "kim ",
        "ahn ", "sumin", "su-min", "168.", "apkmody", "flashscore", "cocomelon", "articoolo",
        "hollyweed", "meridial", "walmart", "what is an nft", "claude", "ami marketplace",
        "salami", "bvn", "teror", "cancel the evil", "bad influencer", "newbisanara",
        "a love other than yours", "see you at work", "military", "103", "daur bumi",
        "igaming", "eu ai act", "ai news today", "grok", "content rewards", "concepts")
queries = {}
for kw, d in raw.get("related_queries", {}).items():
    if not isinstance(d, list) or not d:
        continue
    bagus = []
    for r in d:
        q = r.get("query", "").strip()
        if q and not any(j in q.lower() for j in JUNK):
            bagus.append(q)
    queries[kw] = bagus

baris = []

def add(kat, topik, kw_list, skor, url=URL):
    baris.append(dict(zip(H1, (TGL, kat, topik, "; ".join(kw_list[:6]),
                               "Google Trends (Related Queries - Rising)", "naik", str(skor), "netral", url))))

# TikTok Shop: ekosistem penjual & kreator
qs = queries.get("tiktok shop", [])
if qs:
    add("e_commerce", "Ekosistem penjual & kreator TikTok Shop ramai dicari: partner center, creator center, sampai potongan biaya", qs, len(qs))

# WhatsApp Business: API & platform
qs = [q for q in queries.get("whatsapp business", []) if q not in ("what", "whatsapp web com login", "whatsapp website")]
if qs:
    add("industri_digital", "Permintaan WhatsApp Business API naik: pricing, platform, dan integrasi paling dicari pemilik bisnis", qs, len(qs))

# Marketplace: pajak
qs = [q for q in queries.get("marketplace", []) if "pajak" in q.lower()]
if qs:
    add("e_commerce", "Pajak marketplace 2026 masuk daftar pencarian naik - penjual mulai menghitung kewajiban pajaknya", qs, len(qs))

# AI content: perencanaan konten
qs = [q for q in queries.get("ai content", []) if "content" in q.lower()]
if qs:
    add("industri_digital", "Perencanaan konten jadi kebutuhan pemasar: content calendar, strategy, dan brief dicari naik seiring adopsi AI", qs, len(qs))

# Influencer: regulasi & media kit
qs = [q for q in queries.get("influencer", []) if "ojk" in q.lower() or "media kit" in q.lower()]
if qs:
    add("media_sosial", "Regulasi influencer mulai disorot publik: denda OJK dicari naik, media kit jadi kebutuhan kreator", qs, len(qs))

# Website
qs = [q for q in queries.get("website toko online", []) if "jasa" in q.lower()]
if qs:
    add("teknologi", "Jasa pembuatan website naik sebagai pencarian - bisnis mulai bangun kanal sendiri", qs, len(qs))

# Interest 12 bulan: hanya yang naik + insight pergeseran
for k, d in raw.items():
    if not k.startswith("iot12_") or k.endswith("_error"):
        continue
    for kw, m in d.items():
        if m["last"] > m["first"] * 1.15:
            add("industri_digital", f"Minat pencarian '{kw}' muncul dan naik dalam 12 bulan terakhir (skor {int(m['first'])} -> {int(m['last'])})", [kw], int(m["avg"]))

# tulis (dedupe)
rows = list(csv.DictReader(open("data/tren_topik.csv", encoding="utf-8-sig")))
ada = {"|".join(r[k].strip().lower() for k in ("kategori", "topik")) for r in rows}
n = 0
for b in baris:
    key = (b["kategori"] + "|" + b["topik"]).lower()
    if key not in ada:
        rows.append(b); ada.add(key); n += 1
with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1); w.writeheader(); w.writerows(rows)
print(f"tren_topik.csv: +{n} baris narasi baru (total {len(rows)})")

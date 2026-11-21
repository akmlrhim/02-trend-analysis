# -*- coding: utf-8 -*-
"""Tambahkan isu terkini (berita industri & platform) ke data/tren_topik.csv.

Sumber: Google News RSS 7 hari terakhir (query sama seperti refresh_weekly.py).
Hanya baris relevan agensi digital marketing / jasa digital yang disimpan;
topik yang sudah ada dilewati (dedupe memakai judul yang dinormalisasi).
Dijalankan manual: python scripts/scraping/refresh_isu_terkini.py
"""
import csv
import html
import re
import sys
import urllib.parse
import urllib.request
from datetime import date

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = date.today().isoformat()
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber",
      "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

QUERIES = [
    ("site:campaignindonesia.id when:7d", "Campaign Indonesia", "industri_digital"),
    ('(digital marketing OR "iklan digital" OR "media sosial") Indonesia when:7d',
     "Google News RSS", "industri_digital"),
    ('(TikTok Shop OR "TikTok" OR Instagram OR "Meta Ads") Indonesia when:7d',
     "Google News RSS", "media_sosial"),
    ('(UMKM digital OR e-commerce OR marketplace) Indonesia when:7d',
     "Google News RSS", "industri_digital"),
]

# Topik di luar industri owner (politik, olahraga, selebriti, PR award)
BLOKIR = re.compile(
    r"(jokowi|prabowo|fadli|gibran|pemilu|presiden|dpr|polri|komdigi|gerindra|pdip|"
    r"golkar|megawati|raffi|timnas|u-17|kamboja|afghanistan|avril lavigne|"
    r"balikpapan|barito|deportivo|puebla|basket|nba|bola|badai|marinir|bbm)", re.I)
RELEVAN = re.compile(
    r"(iklan|advertis|digital|media sosial|social media|tiktok|instagram|meta|"
    r"facebook|e-?commerce|marketplace|umkm|konten|content|kreator|creator|"
    r"affiliate|brand|kampanye|agensi|gaming|gta|shopee|tokopedia|grab|"
    r"monetisasi|follower|reach|ads|influencer)", re.I)
PR_SPAM = re.compile(r"(raih|sabet|apresiasi|diterima|champion|penghargaan)", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def ambil():
    hasil = []
    for q, sumber, kategori in QUERIES:
        url = ("https://news.google.com/rss/search?q=" + urllib.parse.quote(q)
               + "&hl=id&gl=ID&ceid=ID:id")
        try:
            xml = get(url)
        except Exception as e:
            print(f"  gagal '{q[:40]}': {e}")
            continue
        n = 0
        for m in re.finditer(r"<item>([\s\S]*?)</item>", xml):
            b = m.group(1)
            judul = html.unescape(re.sub(r"\s*-\s*[^-]+$", "", (re.search(r"<title>([\s\S]*?)</title>", b) or [None, ""])[1]).strip())
            link = (re.search(r"<link>([\s\S]*?)</link>", b) or [None, ""])[1].strip()
            if not judul or not link or BLOKIR.search(judul) or not RELEVAN.search(judul):
                continue
            if PR_SPAM.search(judul) and "BRI Life" in judul:
                continue
            pct = re.search(r"(\d+(?:[.,]\d+)?)\s*%", judul)
            hasil.append({
                "tanggal_ambil": TGL, "kategori": kategori, "topik": judul,
                "kata_kunci": "", "sumber": sumber, "indikator_tren": "naik",
                "skor_atau_volume": pct.group(1).replace(",", ".") if pct else "",
                "sentimen": "netral", "source_url": link,
            })
            n += 1
            if n >= 12:
                break
        print(f"  {sumber} ({q[:35]}...): {n} kandidat")
    return hasil


def kunci(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()[:70]


path = "data/tren_topik.csv"
with open(path, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    header, rows = reader.fieldnames, list(reader)

ada = {kunci(r["topik"]) for r in rows}
baru = []
for r in ambil():
    k = kunci(r["topik"])
    if k in ada:
        continue
    ada.add(k)
    baru.append(r)

for r in baru:
    rows.append({**{h: "" for h in header}, **r})

with open(path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    w.writerows(rows)

print(f"tren_topik.csv: +{len(baru)} isu baru -> {len(rows)} baris")
for r in baru:
    print(" -", r["kategori"], "|", r["topik"][:90])

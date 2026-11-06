# -*- coding: utf-8 -*-
"""Refresh mingguan data tren untuk agensi digital marketing.
Mengambil data baru (trends, berita industri, X/TikTok trending, autocomplete),
menambahkan baris relevan-industri ke CSV yang sudah ada (dengan dedupe),
lalu menormalisasi format. File kalender/checklist/referensi tidak diubah.
Jalankan dari root: python scripts/refresh_weekly.py
"""
import csv, re, subprocess, sys, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
TGL = None  # diisi dari sistem
from datetime import date, datetime, timedelta
TGL = date.today().isoformat()

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

# Blok kata politik/berita umum agar X trending tetap relevan industri
BLOKIR = ["jokowi", "prabowo", "presiden", "dpr", "polri", "polisi", "gibran", "pemilu",
          "savepresiden", "komdigi", "menhan", "gerindra", "pdip", "golkar", "sby", "megawati",
          "roy suryo", "suket", "ijazah"]
JUNK_X = re.compile(r"\d{1,2}\s+(Nov|Des|Jan|Feb|Okt|Aug|Sep)\b|WIB$|\d{1,2}:\d{2}")

def x_trending():
    """Trending X Indonesia via lagitren.id, difilter blok kata politik."""
    try:
        t = get("https://lagitren.id/twitter")
        items = re.findall(r">([^<>]{3,60})<\/(?:a|span|td|h3|li|p)>", t)
        ada = [i.strip() for i in items if 3 < len(i.strip()) < 60]
        mulai = ada.index("X (Twitter) Trending") if "X (Twitter) Trending" in ada else 0
        hasil = []
        for i in ada[mulai + 1:]:
            if i.startswith(("Google", "YouTube", "Instagram", "TikTok", "Netflix", "Produk")) or "tren" in i.lower():
                break
            if JUNK_X.search(i):
                continue
            if any(b in i.lower() for b in BLOKIR):
                continue
            hasil.append(i)
        return hasil[:15]
    except Exception as e:
        print(f"  X trending gagal: {e}")
        return []

def berita_industri():
    """Berita industri 7 hari terakhir: Tempo, Campaign Indonesia, query umum."""
    hasil = []
    queries = [
        ("site:campaignindonesia.id when:7d", "Campaign Indonesia"),
        ("site:tempo.co digital marketing OR iklan OR \"media sosial\" when:7d", "Tempo.co"),
        ("(digital marketing OR \"tiktok ads\" OR \"meta ads\") Indonesia when:7d", "Google News RSS"),
    ]
    for q, sumber in queries:
        try:
            t = get(f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=id&gl=ID&ceid=ID:id")
            for m in re.finditer(r"<item>([\s\S]*?)</item>", t):
                b = m.group(1)
                judul = re.sub(r"\s*-\s*Tempo\.co.*$", "", re.sub(r"\s*-\s*Campaign Indonesia.*$", "",
                    (re.search(r"<title>([\s\S]*?)</title>", b) or [None, ""])[1].strip()))
                if judul and not any(b2 in judul.lower() for b2 in BLOKIR):
                    hasil.append((judul, sumber))
        except Exception as e:
            print(f"  berita '{q[:40]}' gagal: {e}")
    return hasil[:15]

def tiktok_trending():
    """Trending TikTok via agregator socialmediadefined (views diambil bila terbaca)."""
    try:
        t = get("https://socialmediadefined.com/id/trending")
        rows = re.findall(
            r"@([\w.\- ]{2,30})\s*·\s*▶\s*([\d,.]+)", t)
        return [(u, int(v.replace(",", ""))) for u, v in rows[:10]]
    except Exception as e:
        print(f"  TikTok trending gagal: {e}")
        return []

def autocomplete():
    """Pertanyaan industri dari Google autocomplete (prefix tetap)."""
    prefixes = ["cara iklan", "tiktok affiliate", "cara naikkan followers", "umkm online",
                "jasa buat website", "digital marketing", "cara promosi", "meta ads"]
    hasil = []
    for p in prefixes:
        try:
            t = get(f"https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=ID&q={urllib.parse.quote(p)}")
            for s in re.findall(r'"([^"]{6,80})"', t)[1:6]:
                if s != p and not s.startswith("ERROR"):
                    hasil.append(s)
        except Exception as e:
            print(f"  autocomplete '{p}' gagal: {e}")
    return hasil[:25]

def tambah_baris(path, header, baris_baru, kunci):
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    ada = {"|".join(r[k].strip().lower() for k in kunci) for r in rows}
    n = 0
    for r in baris_baru:
        key = "|".join(r[k].strip().lower() for k in kunci)
        if key not in ada:
            rows.append({**{h: "" for h in header}, **r})
            ada.add(key)
            n += 1
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    return n, len(rows)

print(f"Refresh mingguan - {TGL}")

# 1. pytrends (opsional, rate limit aman)
print("1) pytrends...")
try:
    subprocess.run([sys.executable, "scripts/scraping/pytrends_run.py"], check=True, timeout=300)
    print("  OK - data/_pytrends_raw.json diperbarui")
except Exception as e:
    print(f"  dilewati: {e}")

# 2. X trending
print("2) X trending...")
d1_baru = []
for i, tag in enumerate(x_trending(), 1):
    d1_baru.append(dict(zip(H1, (TGL, "media_sosial", f"Trending X: {tag}", tag,
        "X Trending (agregator lagitren.id)", "naik", "", "netral", "https://lagitren.id/twitter"))))

# 3. Berita industri
print("3) Berita industri...")
for judul, sumber in berita_industri():
    d1_baru.append(dict(zip(H1, (TGL, "industri_digital", judul, "", sumber, "naik", "", "netral",
        f"https://news.google.com/rss/search?q=site:{'campaignindonesia.id' if sumber == 'Campaign Indonesia' else 'tempo.co'}+when:7d&hl=id&gl=ID&ceid=ID:id"))))

# 4. TikTok trending
print("4) TikTok trending...")
for u, v in tiktok_trending():
    d1_baru.append(dict(zip(H1, (TGL, "media_sosial", f"Trending TikTok: @{u}", "#fyp",
        "TikTok Trending (agregator socialmediadefined.com)", "naik", str(v), "netral",
        "https://socialmediadefined.com/id/trending"))))

n1, tot1 = tambah_baris("data/tren_topik.csv", H1, d1_baru, ["kategori", "topik"])
print(f"  tren_topik.csv: +{n1} baris baru (total {tot1})")

# 5. Autocomplete
print("5) Autocomplete industri...")
UA2 = "https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=ID&q="
d2_baru = []
for s in autocomplete():
    d2_baru.append(dict(zip(H2, (TGL, "industri_digital", s, "Google Autocomplete", "", UA2 + urllib.parse.quote(s.replace(" ", "+"))))))
n2, tot2 = tambah_baris("data/pertanyaan_audiens.csv", H2, d2_baru, ["pertanyaan_atau_keluhan"])
print(f"  pertanyaan_audiens.csv: +{n2} baris baru (total {tot2})")

# 6. Normalisasi format
print("6) Normalisasi...")
subprocess.run([sys.executable, "scripts/dataset/normalize_data.py"], check=True, timeout=120)
print("Selesai. Dashboard akan memuat data baru saat dibuka ulang (cache Streamlit per URL proses).")

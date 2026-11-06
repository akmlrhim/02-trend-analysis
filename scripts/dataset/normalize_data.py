# -*- coding: utf-8 -*-
"""Normalisasi data: format sumber, topik, skor numerik, dan nilai antar-file yang seragam.
Jalankan dari root: python scripts/dataset/normalize_data.py"""
import csv, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from datetime import date
TGL = date.today().isoformat()  # tanggal ambil = hari refresh dijalankan

# ---------- DATASET 1: tren_topik.csv ----------
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
d1 = list(csv.DictReader(open("data/tren_topik.csv", encoding="utf-8-sig")))

def norm_topik(t):
    t = t.replace("Related query RISING:", "Terkait naik:").replace("Related query TOP:", "Terkait populer:")
    t = t.replace("Interest over time 12 bulan:", "Interest 12 bulan:")
    t = t.replace("X trending:", "Trending X:").replace("TikTok trending:", "Trending TikTok:")
    t = t.replace("YouTube trending ID:", "Trending YouTube:")
    t = t.replace("Hashtag TikTok naik:", "Hashtag TikTok:")
    t = t.replace("Hashtag IG volume besar (global):", "Hashtag Instagram (global):")
    t = t.replace("Kategori Reels IG naik Nov 2026 (global):", "Kategori Reels Instagram (global):")
    return t.strip()

def norm_sumber1(s):
    # Nama kanonik sudah benar: biarkan apa adanya
    kanonik = {"Google Trends (Trending Now)", "Google Trends (Interest Over Time)",
               "Google Trends (Related Queries - Rising)", "Google Trends (Related Queries - Top)",
               "Google News RSS", "X Trending (agregator lagitren.id)",
               "TikTok Trending (agregator socialmediadefined.com)",
               "YouTube Trending (agregator CreatorDB)", "Instagram Hashtag (agregator iqhashtags)",
               "Instagram Hashtag (agregator Dash Social)", "Analisis marketplace (artikel Accio)",
               "Tempo.co", "Campaign Indonesia", "Berita industri digital (via tavily)"}
    if s in kanonik:
        return s
    s2 = s.lower()
    if "trending now" in s2: return "Google Trends (Trending Now)"
    if "interest over time" in s2: return "Google Trends (Interest Over Time)"
    if "related queries (rising)" in s2: return "Google Trends (Related Queries - Rising)"
    if "related queries (top)" in s2: return "Google Trends (Related Queries - Top)"
    if s.startswith("Berita via Google News RSS") or s.startswith("Google News RSS"): return "Google News RSS"
    if s == "Tempo.co" or s.startswith("Tempo.co"): return "Tempo.co"
    if s == "Campaign Indonesia" or s.startswith("Campaign Indonesia"): return "Campaign Indonesia"
    if "lagitren" in s2: return "X Trending (agregator lagitren.id)"
    if "socialmediadefined" in s2: return "TikTok Trending (agregator socialmediadefined.com)"
    if "creatordb" in s2 or "youtrendings" in s2: return "YouTube Trending (agregator CreatorDB)"
    if "iqhashtags" in s2: return "Instagram Hashtag (agregator iqhashtags)"
    if "dash social" in s2: return "Instagram Hashtag (agregator Dash Social)"
    if "accio" in s2 or "tokopedia blog" in s2: return "Analisis marketplace (artikel Accio)"
    return "Berita industri digital (via tavily)"

def norm_skor(v):
    v = v.strip()
    if not v: return ""
    m = re.match(r"avg=([\d.]+),", v)
    if m: return str(int(float(m.group(1))))
    m = re.match(r"([\d.,]+)%$", v)
    if m: return m.group(1).replace(",", "")
    m = re.match(r"(\d[\d.]*)\+$", v)
    if m: return m.group(1).replace(".", "")
    m = re.match(r"(views|usd|posts|users)=(\d+)$", v)
    if m: return m.group(2)
    return v.replace(",", "") if v.replace(",", "").isdigit() else v

for r in d1:
    r["tanggal_ambil"] = TGL
    r["topik"] = norm_topik(r["topik"])
    r["sumber"] = norm_sumber1(r["sumber"])
    r["skor_atau_volume"] = norm_skor(r["skor_atau_volume"])
    r["sentimen"] = r["sentimen"].strip().lower()
    r["indikator_tren"] = r["indikator_tren"].strip().lower()

with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1); w.writeheader(); w.writerows(d1)
kosong_url1 = sum(1 for r in d1 if not r["source_url"])
print(f"tren_topik.csv: {len(d1)} baris | sumber unik: {len({r['sumber'] for r in d1})} | source_url kosong: {kosong_url1}")

# ---------- DATASET 2: pertanyaan_audiens.csv ----------
H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]
d2 = list(csv.DictReader(open("data/pertanyaan_audiens.csv", encoding="utf-8-sig")))

def norm_sumber2(s):
    s2 = s.lower()
    if "autocomplete" in s2: return "Google Autocomplete"
    if "trends" in s2 and "related" in s2: return "Google Trends (Related Queries)"
    if "reddit" in s2: return "Reddit r/indonesia"
    if "kaskus" in s2: return "Kaskus"
    if "google news" in s2: return "Google News RSS"
    return "Berita industri (via tavily)"

for r in d2:
    r["tanggal_ambil"] = TGL
    r["kategori"] = r["kategori"].strip().lower()
    r["sumber"] = norm_sumber2(r["sumber"])
    r["frekuensi_atau_jumlah_mention"] = r["frekuensi_atau_jumlah_mention"].replace("%", "").strip()

with open("data/pertanyaan_audiens.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H2); w.writeheader(); w.writerows(d2)
kosong_url2 = sum(1 for r in d2 if not r["source_url"])
print(f"pertanyaan_audiens.csv: {len(d2)} baris | sumber unik: {len({r['sumber'] for r in d2})} | source_url kosong: {kosong_url2}")

# ---------- DATASET 5: kalender_momen.csv ----------
H5 = ["tanggal", "nama_momen", "jenis", "relevansi", "catatan", "source_url"]
d5 = list(csv.DictReader(open("data/kalender_momen.csv", encoding="utf-8-sig")))
JENIS_OK = {"hari_besar", "libur_nasional", "musim_belanja", "gajian", "event_industri", "event_viral"}
map_jenis = {"hari libur": "libur_nasional"}
for r in d5:
    j = r["jenis"].strip().lower().replace(" ", "_")
    r["jenis"] = j if j in JENIS_OK else map_jenis.get(j, j)
    r["relevansi"] = r["relevansi"].strip().lower()
    r["tanggal"] = r["tanggal"].strip()
with open("data/kalender_momen.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H5); w.writeheader(); w.writerows(d5)
bad5 = [r["jenis"] for r in d5 if r["jenis"] not in JENIS_OK]
print(f"kalender_momen.csv: {len(d5)} baris | jenis di luar kamus: {bad5 or 'tidak ada'}")

# ---------- CHECKLIST: jumlah_baris numerik ----------
HC = ["dataset", "sumber", "status", "jumlah_baris", "tool_yang_dipakai", "alasan_jika_gagal"]
ck = list(csv.DictReader(open("data/_sumber_checklist.csv", encoding="utf-8-sig")))
for r in ck:
    v = r["jumlah_baris"].strip()
    if "+" in v and all(p.strip().isdigit() for p in v.split("+")):
        r["jumlah_baris"] = str(sum(int(p) for p in v.split("+")))
with open("data/_sumber_checklist.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=HC); w.writeheader(); w.writerows(ck)
print(f"_sumber_checklist.csv: {len(ck)} baris | jumlah_baris kini semua numerik")

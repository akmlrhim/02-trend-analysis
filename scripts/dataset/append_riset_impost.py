# -*- coding: utf-8 -*-
"""Riset khusus Impost Media (6 Nov 2026): isu industri 30 hari terakhir yang tervalidasi
2+ sumber. Jalankan dari root: python scripts/dataset/append_riset_impost.py"""
import csv, sys
from datetime import date
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = date.today().isoformat()
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
URL_TAVILY = "https://tavily.com"

baris = [
    # Isu 1: Meta larang iklan TikTok (validasi: Reuters via Kontan 8/10, Kompas 9/10, IDN Times)
    dict(zip(H1, (TGL, "industri_digital",
        "Meta larang iklan ByteDance/TikTok di FB & IG sejak 8 Okt 2026 di 7 negara termasuk Indonesia",
        "meta ads; tiktok; kebijakan platform", "Reuters via Kontan (8 Okt 2026)", "naik", "", "negatif",
        "https://internasional.kontan.co.id/news/meta-blokir-iklan-tiktok-di-facebook-dan-instagram-berlaku-juga-di-indonesia"))),
    dict(zip(H1, (TGL, "industri_digital",
        "Kompas: Meta setop iklan TikTok di 7 negara termasuk Indonesia sejak 8 Okt 2026",
        "meta ads; tiktok; kebijakan platform", "Kompas.com (9 Okt 2026)", "naik", "", "negatif",
        "https://money.kompas.com/read/2026/10/09/095339026/meta-setop-iklan-tiktok-di-7-negara-termasuk-indonesia"))),
    # Isu 2: Digital 2027 Indonesia (5 Nov 2026)
    dict(zip(H1, (TGL, "industri_digital",
        "Digital 2027 (DataReportal): TikTok ad reach Indonesia 240 juta pengguna 18+, naik 33,3% (6,00 juta) dari akhir 2025",
        "tiktok; ad reach; digital 2027", "DataReportal Digital 2027 Indonesia (Nov 2026)", "naik", "240000000", "positif",
        "https://datareportal.com/reports/digital-2027-indonesia"))),
    # Isu 3: AI search menggerus klik organik
    dict(zip(H1, (TGL, "teknologi",
        "Studi Ahrefs (Feb 2026, 300 ribu keyword): AI Overview berkorelasi dengan CTR halaman ranking 1 turun rata-rata 58%",
        "ai overviews; seo; ctr", "Ahrefs via Search Counsel (Feb 2026)", "naik", "", "negatif",
        "https://searchcounselco.com/google-ai-mode-seo-2026-traffic-impact"))),
    dict(zip(H1, (TGL, "teknologi",
        "Google ubah tata letak tautan di AI Mode & AI Overviews (15 Okt 2026): tautan inline naik, kotak situs resmi, carousel berita",
        "ai mode; google search; seo", "Analisis praktisi (update Google 15 Okt 2026)", "naik", "", "netral",
        "https://searchcounselco.com/google-ai-mode-seo-2026-traffic-impact"))),
    # Isu 4: 11.11 & Q4
    dict(zip(H1, (TGL, "e_commerce",
        "Kalender Q4 2026: 11.11 (11 Nov) dan Black Friday jadi puncak belanja online Indonesia",
        "11.11; black friday; e-commerce", "SIRCLO Indonesia Q4 E-Commerce Calendar (2026)", "naik", "", "positif",
        "https://sirclo.com/featured-insights/trend/indonesia-q4-e-commerce-calendar-2026"))),
    # Isu 5: Meta ads bergeser AI
    dict(zip(H1, (TGL, "industri_digital",
        "Meta Ads 2026: Advantage+ jadi kampanye default, targeting detail hanya 'saran' - relevansi kreatif yang menentukan",
        "advantage+; andromeda; meta ads", "Hawky AI changelog (ref Jon Loomer, 2026)", "naik", "", "netral",
        "https://hawky.ai/blog/meta-ads-updates-2026"))),
    # Konteks: regulasi PDP
    dict(zip(H1, (TGL, "regulasi",
        "PP 33/2026 (pelaksana UU PDP) terbit; kerangka implementasi berlaku 16 Jan 2027 - bisnis pemilik data wajib patuh",
        "pdp; perlindungan data; regulasi", "Hukumonline (2026)", "naik", "", "netral",
        "https://pro.hukumonline.com/a/lt6a97c3fe4527c/pemerintah-akhirnya-terbitkan-kerangka-implementasi-pelindungan-data-pribadi--berlaku-mulai-16-januari-2027"))),
]

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
print(f"tren_topik.csv: +{n} baris riset Impost Media (total {len(rows)})")

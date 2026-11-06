# -*- coding: utf-8 -*-
"""Penyesuaian final: sisihkan baris non-industri tersisa, tambahkan isu industri terbaru (Nov 2026)."""
import csv, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TGL = "2026-11-06"
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]

d1 = list(csv.DictReader(open("data/tren_topik.csv", encoding="utf-8-sig")))

# X trending politik/pemerintahan & baris gadget konsumen: buang
DROP_TOPIK = {
    "X trending: Jokowi", "X trending: Roy Suryo", "X trending: #savepresiden",
    "X trending: transparansi tanpa tebang pilih", "X trending: wujudkan pembangunan bersama",
    "X trending: sumber daya manusia unggul", "X trending: 75th Humas Mengabdi",
    "X trending: Tailor", "X trending: Trip", "X trending: WOULD YOU TAKE MY RING",
    "Jadwal rilis HyperOS 4 untuk Xiaomi/Redmi/Poco",
    "Interest over time 12 bulan: smartphone",
    "Related query RISING: best smartphone 2026", "Related query RISING: foldable smartphone",
    "Related query TOP: smartphone samsung", "Related query TOP: harga smartphone", "Related query TOP: smartphone 5g",
}
d1 = [r for r in d1 if r["topik"] not in DROP_TOPIK]

BARU1 = [
    ("industri_digital", "MMA IMPACT 2026: pendapatan iklan digital Indonesia diproyeksikan US$16,8 miliar pada 2030, naik dari US$10,7 miliar (2025)",
     "iklan digital; ad spend; mma impact",
     "Republika Online (liputan MMA IMPACT 2026)", "naik", "usd=16800000000", "positif",
     "https://ekonomi.republika.co.id/berita/tnpid5370/mma-impact-2026-bahas-strategi-pemasaran-untuk-mendorong-pertumbuhan-bisnis"),
    ("e_commerce", "Transaksi fesyen TikTok Shop by Tokopedia melonjak 70% pada Semester I 2026, ditopang video pendek dan LIVE",
     "tiktok shop; live shopping; fashion",
     "Fortune Indonesia", "naik", "", "positif",
     "https://www.fortuneidn.com/business/transaksi-fesyen-tiktok-shop-melonjak-70-pada-semester-i-2026-00-4vfn9-3flpwd"),
]
existing = {r["topik"] for r in d1}
for vals in BARU1:
    row = dict(zip(H1, (TGL,) + vals))
    if row["topik"] not in existing:
        d1.append(row)

with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1)
    w.writeheader()
    w.writerows(d1)
print(f"tren_topik.csv: {len(d1)} baris")

# ---------- DATASET 2 ----------
H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]
d2 = list(csv.DictReader(open("data/pertanyaan_audiens.csv", encoding="utf-8-sig")))
DROP2_KAT = {"telekomunikasi", "internet", "produktivitas"}
DROP2_Q = {
    "cara membuat email baru", "cara daftar driver shopee food", "apa itu denda kafarat",
    "cara download wa di laptop",
    "kenapa hp cepat panas", "kenapa hp tidak bisa di cas", "kenapa hp bisa mati sendiri",
    "kenapa hp tiba tiba mati", "kenapa hp sering panas", "kenapa hp ada iklan terus",
    "kenapa hp iphone tiba tiba mati sendiri",
    "berapa harga iphone 17 pro max", "berapa harga iphone 13", "berapa harga iphone 18 pro max",
    "kenapa harga ram naik", "kenapa harga laptop naik",
    "Apakah Reddit clone versi lokal bisa dibuat di Indonesia?",
    "Thread komparasi dan konsultasi sebelum membeli perangkat elektronik",
}
d2 = [r for r in d2 if r["kategori"] not in DROP2_KAT and r["pertanyaan_atau_keluhan"] not in DROP2_Q]

# tambahan: iklan Google Maps (hasil autocomplete industri)
row = dict(zip(H2, (TGL, "industri_digital", "cara iklan di google maps",
                    "Google autocomplete (suggest API, hl=id gl=ID)", "",
                    "https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=ID&q=cara+iklan+di+google+maps")))
if row["pertanyaan_atau_keluhan"] not in {r["pertanyaan_atau_keluhan"] for r in d2}:
    d2.append(row)

with open("data/pertanyaan_audiens.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H2)
    w.writeheader()
    w.writerows(d2)
print(f"pertanyaan_audiens.csv: {len(d2)} baris")

# checklist
rows = list(csv.reader(open("data/_sumber_checklist.csv", encoding="utf-8-sig")))
rows.append(["1-2", "Penyesuaian final relevansi: buang X trending politik, gadget konsumen (smartphone/HyperOS/iPhone), telko/internet konsumen, produk sisa; tambah MMA IMPACT 2026 (ad spend US$16,8 M proyeksi 2030) & TikTok Shop fashion +70%", "berhasil", "2+1", "tavily + python csv", ""])
with open("data/_sumber_checklist.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(rows)
print(f"_sumber_checklist.csv: {len(rows)-1} baris")

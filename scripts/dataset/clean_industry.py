# -*- coding: utf-8 -*-
"""Pembersihan data agar relevan dengan industri owner: agensi digital marketing / jasa digital.
Buang baris di luar relevansi (politik, kriminal, lingkungan, kesehatan, dll), tambah baris industri."""
import csv

TGL = "2026-11-06"

# ---------- DATASET 1 ----------
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
with open("data/tren_topik.csv", encoding="utf-8-sig") as f:
    d1 = list(csv.DictReader(f))

DROP1 = {
    "layanan_publik", "keamanan_hiburan", "berita_nasional", "hukum_energi", "politik",
    "politik_keamanan", "politik_internasional", "hukum", "lingkungan", "infrastruktur",
    "energi", "finansial_global", "finansial", "sains", "kesehatan", "keamanan",
    "ekonomi_ketenagakerjaan", "bansos", "kesehatan_sosial", "pangan", "hukum_HAM",
    "olahraga_internasional", "transportasi",
}
d1 = [r for r in d1 if r["kategori"] not in DROP1]

BARU1 = [
    ("industri_digital", "Meta larang iklan TikTok di Facebook & Instagram, Indonesia termasuk 7 negara terdampak (berlaku 8 Okt 2026)",
     "meta ads; larangan iklan tiktok", "Berita teknologi (Selular.id, Kontan, IDNFinancials, aktualita.co)", "naik", "", "negatif",
     "https://selular.id/2026/10/perang-medsos-memanas-meta-larang-iklan-tiktok-di-instagram-dan-facebook"),
    ("industri_digital", "Meta juga menutup tautan yang langsung membuka aplikasi lain (deep-linking) bagi pengiklan",
     "deep linking; kebijakan platform", "IDNFinancials (kutipan kebijakan Meta)", "naik", "", "netral",
     "https://www.idnfinancials.com/id/news/70065/meta-larang-iklan-tiktok-di-instagram-di-7-negara-termasuk-indonesia"),
    ("industri_digital", "Indonesia Digital MeetUp 2026 (SMESCO, 15-16 Okt): 27 juta pelaku UMKM, digitalisasi harus melampaui konten viral",
     "umkm digital; indonesia digital meetup; smesco", "InvestorTrust & BIMNEWS (liputan IDM26)", "naik", "", "netral",
     "https://investortrust.id/business/119423/akselerasi-digitalisasi-umkm-smesco-indonesia-hidupkan-kembali-indonesia-digital-meetup-2026"),
    ("industri_digital", "AI jadi tema utama digitalisasi UMKM: otomatisasi tanpa biaya tinggi, AI fatigue diimbangi konten human-centric",
     "ai marketing; konten autentik; ai fatigue", "Artikel strategi digital marketing 2026 (doel.web.id, imajiku.com)", "naik", "", "netral",
     "https://doel.web.id/tren-digital-marketing-untuk-pertumbuhan-bisnis"),
    ("industri_digital", "Privasi data & transparansi iklan jadi sorotan brand: Menkomdigi tegaskan UU PDP tetap berlaku untuk transfer data Indonesia-AS",
     "uu pdp; perlindungan data pribadi; kepatuhan iklan", "ANTARA (pernyataan Menkomdigi) + artikel strategi brand", "stabil", "", "netral",
     "https://makassar.antaranews.com/berita/623818/menkomdigi-uu-pdp-tetap-berlaku-pada-transfer-data-indonesia-as"),
    ("industri_digital", "Kreator konten keluhkan transparansi penghitungan pendapatan platform; Menekraf respons di WCCE 2026",
     "pendapatan kreator; monetisasi platform", "IDN Times (liputan Menekraf)", "naik", "", "negatif",
     "https://www.idntimes.com/business/economy/kreator-digital-keluhkan-penghasilan-00-bvq5c-mmcvhk"),
    ("industri_digital", "TikTok Awards Indonesia 2026: nominasi Creator of the Year & voting kreator terbuka",
     "tiktok awards; kreator terbaik", "Medcom.id", "naik", "", "positif",
     "https://www.medcom.id/hiburan/montase/0kpqdBnK-daftar-nominasi-tiktok-awards-indonesia-2026-dan-cara-voting-kreator"),
    ("industri_digital", "Pengguna media sosial Indonesia 93 juta+ (2026): basis pasar iklan digital terus tumbuh",
     "statistik media sosial; pengguna aktif", "StateGlobe (data statistik social media Indonesia)", "stabil", "users=93000000", "netral",
     "https://data.stateglobe.com/indonesia/social-media-users-statistics"),
    ("industri_digital", "OJK fasilitasi digitalisasi pembiayaan UMKM (Bulan Inklusif Keuangan)",
     "pembiayaan umkm; ojk digital", "VOI.id (liputan OJK)", "stabil", "", "netral",
     "https://voi.id/ekonomi/599942/dukung-pertumbuhan-ekonomi-ojk-fasilitasi-digitalisasi-pembiayaan-umkm"),
    ("industri_digital", "Kebijakan ekonomi kreatif: akses pembiayaan berbasis kekayaan intelektual untuk pelaku kreatif masih jadi kendala",
     "ekonomi kreatif; hki; pembiayaan kreator", "IDN Times (WCCE 2026)", "stabil", "", "netral",
     "https://www.idntimes.com/business/economy/kreator-digital-keluhkan-penghasilan-00-bvq5c-mmcvhk"),
    ("e_commerce", "Strategi media buying bergeser pasca larangan iklan silang Meta-TikTok: anggaran berpindah ke TikTok Ads & platform lain",
     "media buying; tiktok ads; alokasi anggaran iklan", "Analisis berita (mughu.id, selular.id)", "naik", "", "netral",
     "http://mughu.id/blog/meta-larang-iklan-tiktok-di-facebook-instagram-indonesia"),
]
for vals in BARU1:
    row = dict(zip(H1, (TGL,) + vals))
    if row["topik"] not in {r["topik"] for r in d1}:
        d1.append(row)

with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=H1)
    wr.writeheader()
    wr.writerows(d1)
print(f"tren_topik.csv: {len(d1)} baris, sumber: {len({r['sumber'] for r in d1})}")

# ---------- DATASET 2 ----------
H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]
with open("data/pertanyaan_audiens.csv", encoding="utf-8-sig") as f:
    d2 = list(csv.DictReader(f))

DROP2 = {
    "kesehatan", "psikologi", "sejarah", "politik", "migrasi", "umum", "lingkungan",
    "keamanan", "cuaca", "asuransi", "kepegawaian", "otomotif", "otomotif_bbm",
    "keamanan_digital", "bpjs_kesehatan", "kepegawaian", "gaming",
}
d2 = [r for r in d2 if r["kategori"] not in DROP2]

UA = "https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=ID&q="
BARU2 = [
    ("industri_digital", "cara iklan di instagram", UA + "cara+iklan+di+instagram"),
    ("industri_digital", "cara iklan di facebook", UA + "cara+iklan+di+facebook"),
    ("industri_digital", "cara iklan di tiktok", UA + "cara+iklan+di+tiktok"),
    ("industri_digital", "cara iklan di meta ads", UA + "cara+iklan+di+meta+ads"),
    ("industri_digital", "cara iklan di whatsapp", UA + "cara+iklan+di+whatsapp"),
    ("industri_digital", "cara iklan di threads", UA + "cara+iklan+di+threads"),
    ("industri_digital", "cara iklan di shopee", UA + "cara+iklan+di+shopee"),
    ("industri_digital", "cara iklan di google ads", UA + "cara+iklan+di+google+ads"),
    ("industri_digital", "meta ads adalah", UA + "meta+ads+adalah"),
    ("industri_digital", "tiktok affiliate adalah", UA + "tiktok+affiliate+adalah"),
    ("industri_digital", "cara daftar tiktok affiliate untuk pemula", UA + "tiktok+affiliate+daftar"),
    ("industri_digital", "cara promosi di tiktok", UA + "cara+promosi+di+tiktok"),
    ("industri_digital", "cara promosi di instagram", UA + "cara+promosi+di+instagram"),
    ("industri_digital", "cara promosikan postingan ig", UA + "cara+promosikan+postingan+ig"),
    ("industri_digital", "cara naikkan followers tiktok", UA + "cara+naikkan+followers+tiktok"),
    ("industri_digital", "cara naikkan followers ig", UA + "cara+naikkan+followers+ig"),
    ("industri_digital", "digital marketing kerjanya apa", UA + "digital+marketing+kerjanya+apa"),
    ("industri_digital", "digital marketing agency itu apa", UA + "digital+marketing+agency"),
    ("industri_digital", "copywriting adalah dan contohnya", UA + "copywriting+adalah"),
    ("industri_digital", "copywriting ai: bagaimana memakai AI untuk menulis konten", UA + "copywriting+ai"),
    ("industri_digital", "content creator pemula mulai dari mana", UA + "content+creator+pemula"),
    ("industri_digital", "content creator insight itu apa", UA + "content+creator+insight"),
    ("umkm", "cara jualan online di tiktok", UA + "cara+jualan+online+di+tiktok"),
    ("umkm", "cara jualan online di wa", UA + "cara+jualan+online+di+wa"),
    ("umkm", "cara jualan online untuk pemula", UA + "cara+jualan+online+untuk+pemula"),
    ("umkm", "cara jualan online tanpa modal", UA + "cara+jualan+online+tanpa+modal"),
    ("umkm", "umkm online kena pajak: bagaimana aturannya", UA + "umkm+online+kena+pajak"),
    ("umkm", "pinjaman umkm online pemerintah: syarat dan cara daftar", UA + "pinjaman+umkm+online+pemerintah"),
    ("umkm", "cara bikin qris untuk toko", UA + "cara+bikin+qris+untuk+toko"),
    ("umkm", "jasa buat website toko online: berapa harganya", UA + "jasa+buat+website+toko+online"),
    ("umkm", "jasa buat website murah terpercaya di mana", UA + "jasa+buat+website+murah"),
    ("umkm", "cara daftar umkm online lewat hp", UA + "daftar+umkm+online+lewat+hp"),
    ("umkm", "bantuan umkm online dari pemerintah apa saja", UA + "bantuan+umkm+online"),
]
for kat, q, url in BARU2:
    row = dict(zip(H2, (TGL, kat, q, "Google autocomplete (suggest API, hl=id gl=ID)", "", url)))
    if row["pertanyaan_atau_keluhan"] not in {r["pertanyaan_atau_keluhan"] for r in d2}:
        d2.append(row)

with open("data/pertanyaan_audiens.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=H2)
    wr.writeheader()
    wr.writerows(d2)
print(f"pertanyaan_audiens.csv: {len(d2)} baris, sumber: {len({r['sumber'] for r in d2})}")

# ---------- CHECKLIST: catat pembersihan ----------
with open("data/_sumber_checklist.csv", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))
rows.append(["1-2", "Pembersihan relevansi industri (agensi digital marketing): buang politik/kriminal/lingkungan/kesehatan, tambah isu industri (Meta ban iklan TikTok, IDM26, UU PDP, kreator, TikTok Awards) + 33 pertanyaan industri", "berhasil", "11+33", "python csv + tavily + Google autocomplete", ""])
with open("data/_sumber_checklist.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(rows)
print(f"_sumber_checklist.csv: {len(rows)-1} baris")

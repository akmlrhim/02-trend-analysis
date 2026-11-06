# -*- coding: utf-8 -*-
"""Perluasan riset Impost Media (6 Nov 2026): isu baru 6-9 + tren tambahan.
Semua topik berformat judul narasi, tervalidasi sumber. Jalankan dari root:
python scripts/dataset/append_perluasan.py"""
import csv, sys
from datetime import date
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = date.today().isoformat()
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
HI = ["id_isu", "judul", "ringkasan", "mengapa_peduli", "data_pendukung", "layanan_relevan",
      "sudut_unik", "keyakinan", "urgensi", "prioritas", "sumber_utama", "source_url"]

# ---------- 1. Tren tambahan (narasi, tervalidasi) ----------
baris = [
    # Biaya admin marketplace
    dict(zip(H1, (TGL, "e_commerce",
        "Biaya admin Shopee dihitung dari harga netto (setelah diskon penjual) dengan potongan berlapis hingga 10% plus biaya proses Rp1.250/pesanan",
        "shopee; biaya admin; margin", "Analisis e-commerce Growlab (2026)", "naik", "", "negatif",
        "https://growlab.id/artikel/biaya-admin-marketplace-2026-hitung-dampak-ke-profit"))),
    dict(zip(H1, (TGL, "e_commerce",
        "Tarif admin marketplace 2026: Shopee 2,5-10% (naik di sebagian kategori sejak Jan 2026), Tokopedia cap komisi naik ke Rp650rb/item sejak 18 Mei 2026, TikTok Shop komisi dinamis 2,5-8%",
        "biaya admin; marketplace; margin", "Remarketing.id kalkulator biaya (2026)", "naik", "", "negatif",
        "https://remarketing.id/kalkulator-biaya-admin-marketplace"))),
    dict(zip(H1, (TGL, "e_commerce",
        "Tarif non-star seller marketplace naik dari rata-rata 4,0-5,5% menjadi 6,0-7,5% plus biaya transaksi 1% - margin UMKM makin tipis",
        "shopee; tiktok shop; umkm; margin", "KBS Digital (2026)", "naik", "", "negatif",
        "https://kbsdigital.co.id/umkm/strategi-umkm-agar-tetap-untung"))),
    # Live shopping
    dict(zip(H1, (TGL, "media_sosial",
        "Transaksi TikTok Shop saat sahur Ramadan 2026 naik 15 kali lipat dari hari biasa, didorong hampir sepenuhnya oleh siaran live",
        "live shopping; tiktok shop", "Buzzerpanel analisis live commerce (2026)", "naik", 15, "positif",
        "https://blog.buzzerpanel.id/tiktok-live-shopping-indonesia-2026-strategi-jualan-live"))),
    dict(zip(H1, (TGL, "media_sosial",
        "Live shopping di Indonesia diprediksi bertahan jadi perilaku belanja permanen, bukan tren sesaat",
        "live shopping; perilaku belanja", "Vero ASEAN analisis (2026)", "naik", "", "positif",
        "https://vero-asean.com/live-shopping-trend-in-indonesia-is-here-to-stay"))),
    # Google Ads AI Max
    dict(zip(H1, (TGL, "teknologi",
        "Google resmi meng-upgrade Dynamic Search Ads ke AI Max: pergeseran strategi dari pengelolaan manual ke pertumbuhan berbasis AI",
        "google ads; ai max; dsa", "Pengumuman resmi Google (2026)", "naik", "", "netral",
        "https://business.google.com/us/accelerate/announcements/dsa-upgrade-to-ai-max-2026"))),
    dict(zip(H1, (TGL, "teknologi",
        "AI Max for Search sudah dipakai lebih dari 500.000 pengiklan setahun setelah diluncurkan",
        "ai max; google ads; adopsi", "MediaPost (23 Sep 2026)", "naik", 500000, "netral",
        "https://www.mediapost.com/publications/article/418214/google-adds-ai-max-features-new-gemini-models.html"))),
    dict(zip(H1, (TGL, "teknologi",
        "Google Ads luncurkan laporan Search terms & ad combinations untuk kampanye AI Max (13 Okt 2026): pengiklan bisa lihat headline dan landing page mana yang disajikan AI per query",
        "ai max; google ads; transparansi", "Common Thread changelog (13 Okt 2026)", "naik", "", "netral",
        "https://commonthreadco.com/blogs/coachs-corner/google-ads-changes-2026"))),
    dict(zip(H1, (TGL, "teknologi",
        "Google tetapkan timeline migrasi AI Max: API lama kehilangan dukungan broad match & ACA bertahap hingga 2027",
        "ai max; migrasi; google ads", "Search Engine Land (Okt 2026)", "naik", "", "netral",
        "https://searchengineland.com/google-sets-ai-max-migration-timeline-for-search-campaigns-485006"))),
    # Influencer
    dict(zip(H1, (TGL, "media_sosial",
        "Indonesia peringkat 2 dunia influencer-driven commerce: 52% konsumen pernah belanja karena rekomendasi influencer",
        "influencer; social commerce", "TechnologyChecker statistik (2026)", "naik", 52, "positif",
        "https://technologychecker.io/blog/influencer-marketing-statistics"))),
    dict(zip(H1, (TGL, "media_sosial",
        "Micro-influencer (10K-100K followers) engagement 3,86% vs mega 1,21% dengan biaya per post 60% lebih murah",
        "micro influencer; engagement; biaya", "Digital Applied statistik (2026)", "naik", 386, "positif",
        "https://www.digitalapplied.com/blog/influencer-marketing-statistics-2026-data-points"))),
    dict(zip(H1, (TGL, "media_sosial",
        "Nano & micro influencer menguasai mayoritas kerja sama brand global (sekitar 54% dari total deal)",
        "nano influencer; micro influencer", "AdIndex State of Influencer Marketing 2026", "naik", 54, "positif",
        "https://adindex.ru/publication/analitics/search/345226/img/2026-State-of-Influencer-Marketing.pdf"))),
    # Data resmi APJII
    dict(zip(H1, (TGL, "industri_digital",
        "Survei resmi APJII 2026: penetrasi internet Indonesia 81,72% atau 235,26 juta jiwa dari 287,3 juta populasi",
        "apjii; pengguna internet; penetrasi", "ANTARA News (Survei APJII 2026)", "naik", 235261078, "netral",
        "https://www.antaranews.com/berita/5576225/survei-apjii-penetrasi-internet-di-indonesia-2026-capai-817-persen"))),
    # Lokal Kalsel
    dict(zip(H1, (TGL, "industri_digital",
        "Adaro Spectapreneur 2026 digelar di Banjarbaru dengan 208 UMKM peserta (21 Okt 2026)",
        "umkm banjarbaru; bazar; kalsel", "Wartabanjar (21 Okt 2026)", "naik", 208, "positif",
        "https://wartabanjar.com/2026/10/21/adaro-spectapreneur-2026-libatkan-208-umkm-di-banjarbaru"))),
    dict(zip(H1, (TGL, "industri_digital",
        "UMKM unggulan Banjarbaru ikut Trade Expo Indonesia ke-41 - produk lokal naik ke panggung nasional",
        "umkm banjarbaru; tei; ekspor", "Lentera Kalimantan (Okt 2026)", "naik", "", "positif",
        "https://lenterakalimantan.com/2026/10/umkm-unggulan-banjarbaru-unjuk-gigi-di-trade-expo-indonesia-2026"))),
]

# ---------- 2. Isu baru (id 6-9) ----------
isu_baru = [
    dict(zip(HI, (6,
        "Biaya Admin Marketplace Naik, Margin Penjual Tergerus",
        "Sepanjang 2026 Shopee, Tokopedia, dan TikTok Shop menaikkan biaya admin/komisi. Shopee menghitung potongan dari harga netto dengan komponen berlapis, Tokopedia menaikkan cap komisi, dan TikTok Shop memakai komisi dinamis. Bagi penjual, potongan berlapis ini langsung memangkas margin tanpa terasa.",
        "Kalau harga jual tidak dihitung ulang, profit bisa habis padahal omzet jalan terus. Pemilik bisnis perlu hitung ulang struktur harga, kelola strategi voucher, dan mulai bangun kanal penjualan sendiri (website/WhatsApp) untuk pembelian berulang tanpa komisi.",
        "Shopee non-star 2,5-10% + biaya proses Rp1.250/pesanan, naik di sebagian kategori sejak Jan 2026 (Remarketing.id) | Tokopedia cap komisi naik ke Rp650rb/item sejak 18 Mei 2026 (Remarketing.id) | Non-star seller naik ke 6,0-7,5% + biaya transaksi 1% (KBS Digital, 2026)",
        "Website & SEO; Digital Ads; Marketplace Management",
        "Agensi lain bahas 'cara jualan di marketplace'. Impost bertanya lebih dulu: 'berapa sisa marginmu sebenarnya?' - lalu tawarkan kalkulator sederhana + jalan keluar membangun kanal sendiri. Sudut lokal: kurir & ongkir Kalsel untuk jangkauan luar kota.",
        "tinggi", "sedang", 6,
        "Remarketing.id kalkulator biaya admin (2026)",
        "https://remarketing.id/kalkulator-biaya-admin-marketplace"))),
    dict(zip(HI, (7,
        "Google Ads Migrasi ke AI Max: Cara Kerja Search Ads Berubah Total",
        "Google resmi meng-upgrade Dynamic Search Ads ke AI Max dan menetapkan timeline migrasi bertahap hingga 2027. AI Max sudah dipakai 500.000+ pengiklan. Pencocokan keyword manual bergeser ke AI - kontrol berpindah ke kualitas halaman tujuan dan data konversi.",
        "Bisnis yang iklan search-nya dikelola 'set-and-forget' bisa boros budget tanpa sadar. Yang untung adalah yang halamannya rapi dan datanya lengkap - justru area yang dikelola agensi.",
        "DSA di-upgrade ke AI Max (pengumuman resmi Google, 2026) | AI Max dipakai 500.000+ pengiklan (MediaPost, 23 Sep 2026) | Laporan Search terms & ad combinations baru mulai 13 Okt 2026 (Common Thread) | Timeline migrasi API hingga 2027 (Search Engine Land)",
        "Digital Ads (Google); Website & SEO",
        "Keyword bukan lagi raja - halaman dan data yang menentukan. Sudut lokal: saat orang Banjarmasin cari 'jasa X', AI menentukan iklan siapa yang tayang; bisnis lokal yang landing page-nya tertata menang murah.",
        "tinggi", "sedang", 7,
        "Pengumuman resmi Google + Search Engine Land (Okt 2026)",
        "https://searchengineland.com/google-sets-ai-max-migration-timeline-for-search-campaigns-485006"))),
    dict(zip(HI, (8,
        "Micro-Influencer: Kanal Termurah dengan Engagement Tertinggi",
        "Indonesia peringkat 2 dunia untuk belanja karena rekomendasi influencer (52% konsumen). Sementara itu data global menunjukkan micro-influencer (10K-100K followers) menghasilkan engagement 3x lebih tinggi dengan biaya 60% lebih murah dibanding selebgram. Kombinasi keduanya membuka peluang besar bagi brand kecil-menengah.",
        "Brand kecil kini bisa beli jangkauan yang dipercaya tanpa budget selebgram. Sebaliknya, asal pilih influencer besar justru pemborosan - engagement mega influencer paling rendah di semua tier.",
        "Influencer-driven commerce Indonesia 52%, peringkat 2 dunia (TechnologyChecker, 2026) | Micro engagement 3,86% vs mega 1,21%, biaya -60% (Digital Applied, 2026) | Nano+micro menguasai ~54% kerja sama brand (AdIndex State of Influencer Marketing 2026)",
        "Produksi Konten; Social Media Management; Branding",
        "Sudut lokal: kreator mikro Banjarmasin/Kalsel jadi jembatan brand lokal ke komunitasnya - tarif masuk akal, audiens relevan. Impost bisa posisi sebagai penyambungnya.",
        "sedang", "sedang", 8,
        "TechnologyChecker + Digital Applied statistik (2026)",
        "https://www.digitalapplied.com/blog/influencer-marketing-statistics-2026-data-points"))),
    dict(zip(HI, (9,
        "Live Shopping Jadi Mesin Penjualan, Bukan Sekadar Hiburan",
        "Belanja lewat siaran live sudah jadi perilaku permanen di Indonesia. Saat momen ramai, transaksi bisa melonjak belasan kali lipat - contohnya transaksi TikTok Shop saat sahur Ramadan 2026 naik 15x dari hari biasa, didorong hampir sepenuhnya oleh live.",
        "UMKM sering mundur karena merasa harus live dengan cara 'heboh'. Padahal live santai yang rutin (cerita restock, tanya-jawab produk) cukup untuk menangkap gelombang belanja ini - plus intensi beli penonton live jauh lebih tinggi dari penonton video biasa.",
        "Transaksi TikTok Shop saat sahur Ramadan 2026 naik 15x, didorong live (Buzzerpanel, 2026) | Live shopping diprediksi jadi perilaku permanen (Vero ASEAN) | TikTok reach Indonesia 240 juta pengguna dewasa (DataReportal Digital 2027)",
        "Produksi Konten; Digital Ads; Social Media Management",
        "Narasi 'live itu harus rame dan bisa jualan' kita balik: live yang konsisten dan jujur lebih menjual daripada live yang heboh tapi episodic. Sudut lokal: live dari workshop/k dukung cerita produk Kalsel.",
        "sedang", "sedang", 9,
        "Buzzerpanel analisis live commerce (2026)",
        "https://blog.buzzerpanel.id/tiktok-live-shopping-indonesia-2026-strategi-jualan-live"))),
]

# ---------- tulis tren (dedupe) ----------
rows = list(csv.DictReader(open("data/tren_topik.csv", encoding="utf-8-sig")))
ada = {"|".join(r[k].strip().lower() for k in ("kategori", "topik")) for r in rows}
n = 0
for b in baris:
    key = (b["kategori"] + "|" + b["topik"]).lower()
    if key not in ada:
        rows.append(b); ada.add(key); n += 1
with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1); w.writeheader(); w.writerows(rows)

# ---------- tulis isu baru (dedupe) ----------
isus = list(csv.DictReader(open("data/isu_impost.csv", encoding="utf-8-sig")))
ada2 = {r["judul"].strip().lower() for r in isus}
n2 = 0
for b in isu_baru:
    if b["judul"].strip().lower() not in ada2:
        isus.append(b); ada2.add(b["judul"].strip().lower()); n2 += 1
with open("data/isu_impost.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=HI); w.writeheader(); w.writerows(isus)

print(f"tren_topik.csv: +{n} baris (total {len(rows)})")
print(f"isu_impost.csv: +{n2} isu (total {len(isus)})")

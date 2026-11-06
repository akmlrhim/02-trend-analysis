# -*- coding: utf-8 -*-
"""Ganti dataset dengan hasil riset terbaru Impost Media (6 Nov 2026).
- Arsipkan tren_topik.csv & referensi_konten.csv lama ke data/_arsip/
- Tulis tren_topik.csv baru (kurasi tervalidasi)
- Tulis isu_impost.csv, ide_konten_impost.csv, jadwal_posting.csv
Jalankan dari root: python scripts/dataset/build_riset_impost.py"""
import csv, os, shutil, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TGL = "2026-11-06"
OS = "data/_arsip"
os.makedirs(OS, exist_ok=True)

# ---------- 1. Arsipkan data lama ----------
for f in ["tren_topik.csv", "referensi_konten.csv"]:
    src, dst = f"data/{f}", f"{OS}/{f.replace('.csv', '_lama_2026-11-06.csv')}"
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)
        print(f"diarsipkan: {f} -> {dst}")

# ---------- 2. tren_topik.csv baru (kurasi riset tervalidasi) ----------
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
rows = []

def add(kat, topik, kw, sumber, ind, skor, sen, url):
    rows.append(dict(zip(H1, (TGL, kat, topik, kw, sumber, ind, str(skor), sen, url))))

# --- Isu 1: Meta larang iklan TikTok ---
add("industri_digital", "Meta larang iklan ByteDance/TikTok di FB & IG sejak 8 Okt 2026 di 7 negara termasuk Indonesia",
    "meta ads; tiktok; kebijakan platform", "Reuters via Kontan (8 Okt 2026)", "naik", "", "negatif",
    "https://internasional.kontan.co.id/news/meta-blokir-iklan-tiktok-di-facebook-dan-instagram-berlaku-juga-di-indonesia")
add("industri_digital", "Kompas: Meta setop iklan TikTok di 7 negara termasuk Indonesia sejak 8 Okt 2026",
    "meta ads; tiktok; kebijakan platform", "Kompas.com (9 Okt 2026)", "naik", "", "negatif",
    "https://money.kompas.com/read/2026/10/09/095339026/meta-setop-iklan-tiktok-di-7-negara-termasuk-indonesia")
add("industri_digital", "UMKM yang arahkan iklan Meta ke TikTok perlu pivot: situs toko, halaman produk, WhatsApp Business",
    "meta ads; whatsapp business; funnel", "IDN Times (Okt 2026)", "naik", "", "netral",
    "https://www.idntimes.com/tech/trend/meta-larang-iklan-tiktok-di-fb-dan-ig-c1c2-01-w8826-577hcw")

# --- Isu 2: Digital 2027 Indonesia ---
add("industri_digital", "Digital 2027 (DataReportal): TikTok ad reach Indonesia 240 juta pengguna 18+, naik 33,3% dari akhir 2025",
    "tiktok; ad reach; digital 2027", "DataReportal Digital 2027 Indonesia (Nov 2026)", "naik", 240000000, "positif",
    "https://datareportal.com/reports/digital-2027-indonesia")
add("industri_digital", "Digital 2027: belanja iklan media sosial Indonesia US$1,80 miliar, naik 16,9%, menyerap 45,3% iklan digital",
    "iklan media sosial; ad spend", "Riset riset pasar via Tavily (5 Nov 2026)", "naik", "", "positif",
    "https://datareportal.com/reports/digital-2027-indonesia")
add("industri_digital", "Digital 2027: 231 juta pengguna internet Indonesia (80,2% populasi) tumbuh hanya 0,4% per tahun - era berebut perhatian",
    "pengguna internet; saturasi", "Riset riset pasar via Tavily (5 Nov 2026)", "naik", 231000000, "netral",
    "https://datareportal.com/reports/digital-2027-indonesia")
add("industri_digital", "Meta Ads 2026: Advantage+ jadi kampanye default, targeting detail hanya 'saran' - kreatif yang menentukan",
    "advantage+; andromeda; meta ads", "Hawky AI changelog (ref Jon Loomer, 2026)", "naik", "", "netral",
    "https://hawky.ai/blog/meta-ads-updates-2026")

# --- Isu 3: AI search ---
add("teknologi", "Studi Ahrefs (Feb 2026, 300 ribu keyword): AI Overview berkorelasi dengan CTR halaman ranking 1 turun rata-rata 58%",
    "ai overviews; seo; ctr", "Ahrefs via Search Counsel (Feb 2026)", "naik", "", "negatif",
    "https://searchcounselco.com/google-ai-mode-seo-2026-traffic-impact")
add("teknologi", "Google ubah tata letak tautan di AI Mode & AI Overviews (15 Okt 2026): tautan inline naik, kotak situs resmi",
    "ai mode; google search; seo", "Analisis praktisi (update Google 15 Okt 2026)", "naik", "", "netral",
    "https://searchcounselco.com/google-ai-mode-seo-2026-traffic-impact")
add("teknologi", "SEO tetap relevan untuk pencarian lokal & transaksional di era AI search (panduan Google)",
    "seo lokal; google business profile", "Global Reach (7 Agu 2026)", "stabil", "", "netral",
    "https://www.globalreach.com/global-reach-media/blog/2026/08/07/2026-ai-search-trends-strategies")

# --- Isu 4: 11.11 & Q4 ---
add("e_commerce", "Kalender Q4 2026: 11.11 (11 Nov) dan Black Friday jadi puncak belanja online Indonesia",
    "11.11; black friday; e-commerce", "SIRCLO Indonesia Q4 E-Commerce Calendar (2026)", "naik", "", "positif",
    "https://sirclo.com/featured-insights/trend/indonesia-q4-e-commerce-calendar-2026")
add("e_commerce", "Promo 11.11 berjalan: Shopee 11.11 s.d. 12 Nov, Segari 10-16 Nov 2026",
    "11.11; promo", "BCA Promo (5 Nov 2026)", "naik", "", "positif",
    "https://promo.bca.co.id/en/all/2026/11/05/08/shopee")
add("e_commerce", "Kalender e-commerce 2026: 11 Nov + Black Friday/Cyber Monday = puncak musim belanja",
    "11.11; black friday", "DHL Indonesia Kalender E-Commerce (2026)", "naik", "", "positif",
    "https://www.dhl.com/discover/id-id/e-commerce-advice/e-commerce-trends/ecommerce-calendar-2026")

# --- Isu 5: UMKM Kalsel ---
add("industri_digital", "DEA 2026 Banjarmasin: 100 pelaku usaha mikro ikuti pelatihan Digital Entrepreneurship Academy fokus video content",
    "umkm banjarmasin; pelatihan", "Instagram event organizer DEA (2026)", "naik", 100, "positif",
    "https://www.instagram.com/reel/DXYlXruj-If")
add("industri_digital", "Dispora Kalsel: 45 peserta pelatihan digitalisasi marketing wirausaha muda (konteks lama, pendukung)",
    "umkm kalsel; pelatihan", "Diskominfo Kalsel (31 Mar 2026)", "stabil", 45, "positif",
    "https://diskominfomc.kalselprov.go.id/2026/03/31/pelatihan-digital-marketing-dispora-kalsel-dorong-wirausaha-muda-adaptif-di-era-perubahan")
add("industri_digital", "Indonesia Digital MeetUp 2026 (SMESCO, 15-16 Okt): 27 juta pelaku UMKM, digitalisasi harus melampaui konten viral",
    "umkm; digitalisasi", "Berita SMESCO via Tavily (Okt 2026)", "naik", 27000000, "netral",
    "https://www.instagram.com/reel/Daj_cngxQMZ")

# --- Regulasi PDP (cadangan) ---
add("regulasi", "PP 33/2026 (pelaksana UU PDP) terbit; kerangka implementasi berlaku 16 Jan 2027 - bisnis pemilik data wajib patuh",
    "pdp; perlindungan data; regulasi", "Hukumonline (2026)", "naik", "", "netral",
    "https://pro.hukumonline.com/a/lt6a97c3fe4527c/pemerintah-akhirnya-terbitkan-kerangka-implementasi-pelindungan-data-pribadi--berlaku-mulai-16-januari-2027")

# --- Riset Instagram (terverifikasi kuantitatif) ---
add("media_sosial", "Algoritma Reels 2026: DM share (sends per reach) sinyal ranking terkuat untuk jangkauan non-follower",
    "sends per reach; dm share", "Statistik industri (vidico/hootsuite 2026)", "naik", "", "netral",
    "https://vidico.com/news/instagram-reels-statistics")
add("media_sosial", "Reels di-share 4,5 miliar kali per hari; ranking Reels naik 10% waktu tontonan Q1 2026",
    "reels share; waktu tontonan", "Statistik industri (hootsuite/creatorflow 2026)", "naik", 4500000000, "netral",
    "https://blog.hootsuite.com/instagram-statistics")
add("media_sosial", "Reels <90 detik dengan jump cut tiap 3-5 detik: engagement +32%, hook 3 detik pertama +72% peluang viral",
    "reels pendek; hook 3 detik", "Statistik industri (loopexdigital 2026)", "naik", 32, "netral",
    "https://www.loopexdigital.com/blog/instagram-reels-statistics")
add("media_sosial", "Reels pakai trending audio: engagement +42%; reach rate rata-rata Reels 30,81%",
    "trending audio; reach reels", "Statistik industri (loopexdigital/demandsage 2026)", "naik", 42, "netral",
    "https://www.loopexdigital.com/blog/instagram-reels-statistics")
add("media_sosial", "Kategori Reels Instagram naik: interior & home decor (26,7K post, Okt 2026)",
    "interiordesign; homedecor", "Instagram Hashtag (agregator Dash Social)", "naik", 26700, "netral",
    "https://www.dashsocial.com/blog/instagram-hashtags")

# --- Rising queries Google Trends (dikelompokkan menjadi judul narasi, bukan tag mentah) ---
raw = json.load(open("data/_instagram_trends_raw.json", encoding="utf-8"))
BUANG = ("download", "downloader", "save.net", "save ", "viewer", "anonim", "anonymously", "snaptik", "convertidor", "mp4", "watermark", "news")
queries = []
for kw, d in raw.get("related_queries", {}).items():
    if not isinstance(d, dict) or d.get("error"):
        continue
    for r in (d.get("rising") or []):
        q = r.get("query", "").strip()
        if q and not any(b in q.lower() for b in BUANG):
            queries.append(q)

GRUP_NARASI = [
    (("capcut",), "Pencarian CapCut template untuk Reels naik tajam di Google Trends Indonesia"),
    (("bio",), "Optimasi bio Instagram jadi kebutuhan: cara menulis bio, emoji, aesthetic bio maker"),
    (("trial reels",), "Fitur Trial Reels Instagram mulai banyak dicari kreator"),
    (("ratio", "ukuran feed"), "Ukuran & rasio konten Instagram dicari naik: reels ratio, ukuran feed 2026"),
]
for kunci, narasi in GRUP_NARASI:
    cocok = [q for q in queries if any(k in q.lower() for k in kunci)]
    if cocok:
        add("media_sosial", narasi, "; ".join(cocok[:5]),
            "Google Trends (Related Queries - Rising)", "naik", len(cocok), "netral",
            "https://trends.google.com/trends/explore?geo=ID")

# --- Interest 12 bulan yang naik (ditulis sebagai narasi) ---
for k, d in raw.items():
    if not k.startswith("iot12_") or k.endswith("_error"):
        continue
    for kw, m in d.items():
        if m["last"] > m["first"] * 1.15:
            add("media_sosial", f"Minat pencarian '{kw}' naik dalam 12 bulan terakhir (skor {int(m['first'])} -> {int(m['last'])})",
                kw, "Google Trends (Interest Over Time)", "naik", int(m["avg"]), "netral",
                "https://trends.google.com/trends/explore?geo=ID")

with open("data/tren_topik.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=H1); w.writeheader(); w.writerows(rows)
print(f"tren_topik.csv baru: {len(rows)} baris (semua topik berformat judul narasi)")

# ---------- 3. isu_impost.csv ----------
HI = ["id_isu", "judul", "ringkasan", "mengapa_peduli", "data_pendukung", "layanan_relevan",
      "sudut_unik", "keyakinan", "urgensi", "prioritas", "sumber_utama", "source_url"]
isu = [
    dict(zip(HI, (1,
        "Meta Melarang Iklan TikTok di Facebook & Instagram",
        "Sejak 8 Oktober 2026, Meta melarang iklan yang mengarahkan orang ke TikTok/ByteDance di Facebook dan Instagram, termasuk di Indonesia. Konten organik tetap boleh, tapi semua funnel iklan berbasis 'klik ke TikTok' langsung mati.",
        "Banyak UMKM menjalankan iklan Meta lalu mengarahkan calon pembeli ke TikTok Shop - sekarang budget tersebut bisa ditolak atau tidak tayang. Funnel harus dipindah ke WhatsApp Business, website, atau katalog sendiri. Salah pindah = uang iklan terbuang.",
        "Reuters via Kontan (8 Okt 2026): kebijakan berlaku di 7 negara termasuk Indonesia | Kompas.com (9 Okt 2026): berlaku efektif 8 Okt | IDN Times (Okt 2026): saran pivot ke situs toko/WA Business",
        "Digital Ads (Meta/TikTok); Website; Social Media Management",
        "Agensi lain bahas 'kebijakannya apa'. Impost bahas 'ke mana uang mengalir': karena Meta menahan orang di aplikasinya, WhatsApp Business jadi funnel paling aman - kebiasaan berjualan yang sudah melekat di Kalsel. 98,8% pengguna internet Indonesia pakai WhatsApp (We Are Social Digital 2026, konteks lama pendukung).",
        "tinggi", "tinggi", 1,
        "Reuters via Kontan (8 Okt 2026)",
        "https://internasional.kontan.co.id/news/meta-blokir-iklan-tiktok-di-facebook-dan-instagram-berlaku-juga-di-indonesia"))),
    dict(zip(HI, (2,
        "Laporan Digital 2027: Iklan Medsos Makin Dominan, TikTok Melesat",
        "Rilis 5 November 2026: iklan media sosial Indonesia menyerap 45,3% dari total iklan digital dan naik 16,9%, sementara reach iklan TikTok naik 33,3% jadi setara 240 juta pengguna dewasa. Tapi pengguna internet baru tumbuh 0,4% per tahun - pasarnya makin sempit, persaingan perhatian makin sengit.",
        "Audiens baru hampir habis; pertumbuhan penjualan online 2027 hanya datang dari mencuri perhatian kompetitor di medsos. Yang belum masang iklan medsos akan kalah harga per perhatian dari yang sudah masuk duluan.",
        "DataReportal Digital 2027 Indonesia: TikTok ad reach 240 juta (18+), naik +33,3% | Belanja iklan medsos US$1,80 M, naik 16,9%, 45,3% dari iklan digital | 231 juta pengguna internet (80,2% populasi), tumbuh 0,4%/tahun",
        "Digital Ads (Meta/TikTok); Social Media Management; Branding",
        "Semua agensi posting 'TikTok 240 juta pengguna!'. Impost balik narasi: 240 juta itu bukan peluang - itu harga. Makin banyak reach, makin ramai pelelangan iklan, CPM naik. Yang menang bukan yang paling masuk, tapi yang kreatifnya paling relevan.",
        "tinggi", "tinggi", 2,
        "DataReportal Digital 2027 Indonesia (Nov 2026)",
        "https://datareportal.com/reports/digital-2027-indonesia"))),
    dict(zip(HI, (3,
        "AI Search Mulai 'Memakan' Klik Organik",
        "Google kini sering menjawab langsung lewat AI Overviews/AI Mode di atas hasil pencarian. Studi besar Februari 2026 menemukan halaman ranking 1 kehilangan rata-rata 58% CTR ketika AI Overview muncul. Tanggal 15 Oktober 2026 Google mengubah tata letak tautan di dalam AI Mode.",
        "Website yang selama ini dapat pembeli dari Google bisa kehilangan aliran itu drastis tanpa ranking-nya turun. Untuk bisnis lokal, kuncinya bergeser ke Google Business Profile, ulasan, dan konten yang 'dikutip AI' (GEO).",
        "Ahrefs (Feb 2026, 300.000 keyword): CTR ranking 1 turun rata-rata 58% saat AI Overview muncul | Update layout AI Mode 15 Okt 2026 | Panduan Google: SEO tetap relevan untuk pencarian lokal & transaksional",
        "Website & SEO; Branding",
        "Konten nasional fokus korporat. Impost ambil sudut kota: 'Ketika orang Banjarmasin nanya AI toko kue terdekat - yang muncul siapa?' AI search bergantung pada data lokal + ulasan, jadi Google Business Profile yang rapi jadi 'SEO baru' bisnis Kalsel.",
        "sedang", "sedang", 4,
        "Ahrefs via Search Counsel (Feb 2026)",
        "https://searchcounselco.com/google-ai-mode-seo-2026-traffic-impact"))),
    dict(zip(HI, (4,
        "Musim Belanja Q4 Dimulai: 11.11 Lima Hari Lagi, Black Friday Menyusul",
        "11.11 (11 November) dan Black Friday adalah puncak belanja online Indonesia di Q4, dengan jendela promo 10-16 November. Ini momen belanja paling panas tahun ini - dan di 2026 terjadi justru setelah kebijakan Meta-TikTok mengubah cara iklan berjalan.",
        "Konsumen sudah dalam mode belanja - yang tidak punya konten/promo siap akan kehilangan momentum ke kompetitor. Kampanye bisa disiapkan bahkan di H-3 dengan format minimal.",
        "SIRCLO Q4 Calendar 2026: 11.11 + Black Friday = fixture utama Q4 | BCA Promo (5 Nov): Shopee 11.11 s.d. 12 Nov, Segari 10-16 Nov | DHL Kalender E-Commerce 2026: 11 Nov + BFCM puncak musim belanja",
        "Digital Ads; Produksi Konten; Marketplace Management",
        "Semua konten 11.11 bicara ke toko online besar. Impost target UMKM yang merasa 'kekecilan' buat ikut 11.11: strategi ikut gelombang tanpa perang diskon - bundling, urgency, konten DM-share. Plus sudut lokal: kurir/ongkir Kalsel, jangkauan luar kota.",
        "tinggi", "tinggi", 3,
        "SIRCLO Indonesia Q4 E-Commerce Calendar (2026)",
        "https://sirclo.com/featured-insights/trend/indonesia-q4-e-commerce-calendar-2026"))),
    dict(zip(HI, (5,
        "Momentum Digitalisasi UMKM Kalsel: Pelatihan Ada, Eksekusi Nol",
        "Sepanjang 2026, Banjarmasin dan Kalsel ramai pelatihan digital: DEA Banjarmasin (100 pelaku usaha mikro, fokus video), pelatihan Dispora Kalsel, dan nasional Indonesia Digital MeetUp (15-16 Okt) yang menyorot 27 juta pelaku UMKM. Masalahnya klasik: semangat naik saat pelatihan, eksekusi berhenti minggu kedua.",
        "Kompetitor lokal yang 'lulus pelatihan' mulai posting dan pasang iklan. UMKM yang berhenti di motivasi akan kehilangan pencarian lokal & jangkauan medsos ke yang konsisten. Digitalisasi juga tidak boleh berhenti di konten viral - harus sampai ke funnel penjualan.",
        "DEA 2026 Banjarmasin: 100 pelaku usaha mikro (IG event organizer) | Diskominfo Kalsel: 45 peserta pelatihan (31 Mar 2026, konteks lama) | Indonesia Digital MeetUp (SMESCO, 15-16 Okt): 27 juta pelaku UMKM",
        "Semua layanan - isu positioning: SMM, Produksi Konten, Digital Ads, Website",
        "Tidak ada agensi Kalsel yang berani bilang: pelatihan itu bagus, tapi pelatihan bukan sistem. Impost mengambil posisi sebagai pelengkap resmi eksekusi pelatihan - alumni DEA/pelatihan Pemkot yang bingung mulai = leads hangat. Narasi: kamu sudah belajar, kami yang eksekusi bareng.",
        "sedang", "sedang", 5,
        "Event lokal DEA Banjarmasin + Diskominfo Kalsel",
        "https://www.instagram.com/reel/DXYlXruj-If"))),
]
with open("data/isu_impost.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=HI); w.writeheader(); w.writerows(isu)
print(f"isu_impost.csv: {len(isu)} isu")

# ---------- 4. ide_konten_impost.csv ----------
HD = ["id_isu", "judul_isu", "nama_ide", "platform", "format", "hook", "poin_isi", "cta", "visual_audio"]
ide = [
    (1, "Meta Melarang Iklan TikTok di Facebook & Instagram",
     "Iklanmu Bisa Ditolak Meta. Cek 3 Hal Ini", "Instagram", "Carousel",
     "Budget iklan hilang gara-gara 1 kebijakan? Banyak pemilik bisnis belum sadar.",
     "Apa yang dilarang sejak 8 Okt | Siapa yang kena (yang arahkan iklan ke TikTok) | Yang tetap aman (konten organik) | 3 funnel pengganti yang disarankan Meta sendiri | Checklist funnel kamu sekarang",
     "Punya iklan jalan? DM 'CEK' - kami audit arah funnel kamu gratis 15 menit.",
     "Mockup layar iklan ditolak, aksen merah-bata, font besar; audio upbeat low-key"),
    (1, "Meta Melarang Iklan TikTok di Facebook & Instagram",
     "Perang Platform, Kamu yang Kena", "TikTok", "Video talking head",
     "Meta dan TikTok perang - dan bisnismu yang jadi medannya.",
     "Cerita kebijakan versi awam | Contoh nyata: iklan IG ke TikTok Shop sekarang bermasalah | Solusi: pisahkan rumah konten dan rumah jualan | Kapan tetap aman pakai TikTok Ads langsung",
     "DM 'FUNNEL' untuk peta funnel 2026.",
     "Potongan layar berita + jump cut tiap 3-5 detik (engagement +32%)"),
    (1, "Meta Melarang Iklan TikTok di Facebook & Instagram",
     "3 Funnel yang Aman dari Kebijakan Meta", "Instagram", "Reels",
     "Kalau iklanmu arahannya ke TikTok, tonton ini dulu.",
     "WhatsApp Business -> balas otomatis -> katalog | Website/Landing Page -> remarketing Meta | Katalog Facebook Shop",
     "Mau funnel yang tahan kebijakan? Konsultasi gratis di bio.",
     "Screen-record WhatsApp Business; audio trending Sean Paul - Give It Up to Me (transisi produk)"),
    (2, "Laporan Digital 2027: Iklan Medsos Makin Dominan, TikTok Melesat",
     "5 Angka Laporan Baru yang Menentukan Bisnismu 2027", "Instagram", "Carousel",
     "Laporan kemarin bilang: audiens baru udah hampir habis.",
     "231 jt pengguna, tumbuh 0,4%/thn = era berebut perhatian | Iklan medsos 45,3% dari digital | TikTok reach +33,3% | Konsekuensi: kreatif > targeting | Langkah pertama owner non-praktisi",
     "Mau tahu posisi bisnismu di peta ini? Konsultasi gratis - link bio.",
     "Angka super besar satu per slide, satu aksen merah-bata; audio netral lo-fi"),
    (2, "Laporan Digital 2027: Iklan Medsos Makin Dominan, TikTok Melesat",
     "TikTok 240 Juta Pengguna: Peluang atau Jebakan?", "TikTok", "Video edukasi",
     "Semua bilang TikTok makin gede. Semua lupa satu hal.",
     "Reach naik tapi iklan juga rame | Efek ke CPM | Cara tetap murah: hook 3 detik + video pendek + DM share",
     "Follow untuk tips iklan yang gak bikin dompet bolong.",
     "Whiteboard/gambar angka; audio trending high-energy"),
    (2, "Laporan Digital 2027: Iklan Medsos Makin Dominan, TikTok Melesat",
     "Kenapa 'Cukup Posting Saja' Sudah Tidak Cukup di 2027", "Instagram", "Reels",
     "Bisnis kamu bersaing dengan 231 juta orang yang juga posting.",
     "Organic reach turun | Sistem: konten -> iklan -> follow-up | Contoh client lokal | Mulai dari 1 funnel",
     "Kami bangun sistemnya - 200+ bisnis Kalsel. Cek bio.",
     "BTS kantor/klien; audio Sometimes - Fleetwood Mac (feel-good, sedang naik)"),
    (3, "AI Search Mulai 'Memakan' Klik Organik",
     "Google Sekarang Menjawab Duluan. Bisnismu Muncul Gak?", "Instagram", "Carousel",
     "Ranking 1 di Google? Klik-mu bisa hilang 58% gara-gara AI.",
     "Apa itu AI Overview (bahasa awam) | Datanya (Ahrefs -58%) | Kenapa bisnis lokal sebenarnya beruntung (local search belum sering digantikan AI) | 3 langkah: GBP lengkap, ulasan aktif, konten yang menjawab pertanyaan",
     "Cek sehat website + Google Business kamu - DM 'SEHAT'.",
     "Simulasi layar pencarian; satu aksen warna per slide"),
    (3, "AI Search Mulai 'Memakan' Klik Organik",
     "Coba Aku Nanya AI: Toko Kue Terdekat di Banjarmasin", "TikTok", "Video demo",
     "Aku nyuruh AI cari toko kue di Banjarmasin. Ini yang muncul.",
     "Demo langsung | Kenapa toko tertentu muncul | 3 hal yang bikin bisnismu 'dipilih' AI | Ulasan = faktor terbesar",
     "Mau bisnismu yang muncul? Konsultasi SEO lokal di bio.",
     "Screen-record asli, jump cut, teks overlay (60% penonton butuh teks)"),
    (3, "AI Search Mulai 'Memakan' Klik Organik",
     "Website Kamu Masih Bergantung Traffic Google? Ini Statistik Barunya", "Instagram", "Reels",
     "Statistik baru: klik ke website bisa turun separuh.",
     "Angka -58% | Yang aman: traffic langsung (IG/TikTok/WA) | Bangun kanal milik sendiri (email/WA list) | Website tetap wajib sebagai rumah",
     "Audit funnel digital gratis untuk 5 bisnis bulan ini.",
     "Grafik turun-naik animasi sederhana; audio dramatic"),
    (4, "Musim Belanja Q4 Dimulai: 11.11 Lima Hari Lagi, Black Friday Menyusul",
     "H-3 11.11: Checklist Darurat Buat Bisnis Kecil", "TikTok", "Video checklist",
     "11.11 tinggal 3 hari - dan kamu belum siap? Tenang, masih kejar.",
     "Pilih 1 hero product | Bundling tanpa membunuh margin | 3 konten wajib: teaser, countdown, live/last call | Setelan iklan minimal: retargeting pengunjung 30 hari",
     "Save video ini. Butuh eksekutor? DM '11.11'.",
     "Checklist cepat, teks besar; audio Timber (fast-cuts, sedang naik)"),
    (4, "Musim Belanja Q4 Dimulai: 11.11 Lima Hari Lagi, Black Friday Menyusul",
     "Ikut 11.11 Tanpa Perang Diskon", "Instagram", "Carousel",
     "Gak harus rugi buat ikut 11.11.",
     "Kenapa gelombang belanja = free traffic | Strategi bundling & nilai tambah | DM share sebagai sinyal algoritma | Contoh promo UMKM",
     "Template promo gratis di bio - tinggal ganti nama produkmu.",
     "Mockup promo, warna hangat; carousel swipe retention"),
    (4, "Musim Belanja Q4 Dimulai: 11.11 Lima Hari Lagi, Black Friday Menyusul",
     "Yang Terjadi Kalau Kamu Skip 11.11 (Skit)", "Instagram", "Reels skit",
     "Skip 11.11 katanya biar hemat iklan... (lalu kompetitor rakus orderan)",
     "Mini-drama | Fakta gelombang belanja Q4 | Minimal action: 1 promo + 3 konten | Ajakan mulai sekarang",
     "Jangan sendirian - tim kami siap eksekusi bulan ini.",
     "Skit 2 tokoh; audio Go Go Juice - Sabrina Carpenter (going-out reveals, naik)"),
    (5, "Momentum Digitalisasi UMKM Kalsel: Pelatihan Ada, Eksekusi Nol",
     "Baru Ikut Pelatihan Digital? 4 Hal yang Bikin Ilmunya Gagal Dipakai", "Instagram", "Carousel",
     "Ikut pelatihan digital 3x tapi akun masih sepi? Ini alasannya.",
     "Pelatihan kasih ilmu, bukan sistem | 4 penghambat: gak konsisten, gak ada funnel, gak diukur, gak ada tim | Minimal: 1 kanal dikelola benar | Cerita alumni/klien",
     "Program pendampingan eksekusi UMKM - kuota bulan ini terbatas. DM 'NAIK KELAS'.",
     "Foto event lokal (tag organizer), sebelum-sesudah akun klien"),
    (5, "Momentum Digitalisasi UMKM Kalsel: Pelatihan Ada, Eksekusi Nol",
     "UMKM Banjarmasin: Latihan Selesai, Sekarang Apa?", "TikTok", "Video storytelling",
     "100 UMKM Banjarmasin baru aja lulus pelatihan video. Ini yang gak mereka kasih tahu.",
     "Apa yang hilang setelah pelatihan | 3 langkah eksekusi pertama | Kenapa konsistensi > viral | Tawaran audit akun gratis",
     "Alumni pelatihan mana pun - audit akun gratis minggu ini.",
     "Lokasi asli Banjarmasin, wajah lokal (relatability = DM share)"),
    (5, "Momentum Digitalisasi UMKM Kalsel: Pelatihan Ada, Eksekusi Nol",
     "Digital Marketing Itu Bukan Konten Viral", "Instagram", "Reels opinion",
     "Konten viral itu bonus. Yang bikin omzet naik bukan itu.",
     "Sejalan tema MeetUp SMESCO | Sistem: dikenal -> dipercaya -> menghasilkan | Contoh alur WA -> closing | Penutup CTA",
     "Bangun sistemnya bareng kami - 200+ bisnis Kalsel.",
     "Talking head + teks; audio Yummy Little Day (wholesome day-in-the-life)"),
]
with open("data/ide_konten_impost.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=HD); w.writeheader(); w.writerows([dict(zip(HD, r)) for r in ide])
print(f"ide_konten_impost.csv: {len(ide)} ide konten")

# ---------- 5. jadwal_posting.csv ----------
HJ = ["tanggal", "isi_konten", "nama_ide", "platform", "isu", "alasan"]
jadwal = [
    ("2026-11-07", "TikTok Checklist Darurat 11.11", "H-3 11.11: Checklist Darurat Buat Bisnis Kecil", "TikTok", "11.11 / Q4", "momentum H-4"),
    ("2026-11-08", "IG Carousel Ikut 11.11 Tanpa Perang Diskon", "Ikut 11.11 Tanpa Perang Diskon", "Instagram Carousel", "11.11 / Q4", "weekend belanja"),
    ("2026-11-10", "IG Reels Skit Skip 11.11", "Yang Terjadi Kalau Kamu Skip 11.11", "Instagram Reels", "11.11 / Q4", "H-1 urgency"),
    ("2026-11-12", "IG Carousel Meta Larang Iklan TikTok", "Iklanmu Bisa Ditolak Meta. Cek 3 Hal Ini", "Instagram Carousel", "Meta-TikTok", "pasca gelombang belanja, budget di-review"),
    ("2026-11-13", "TikTok Perang Platform", "Perang Platform, Kamu yang Kena", "TikTok", "Meta-TikTok", "sebar ke audiens baru"),
    ("2026-11-15", "IG Reels 3 Funnel Aman Meta", "3 Funnel yang Aman dari Kebijakan Meta", "Instagram Reels", "Meta-TikTok", "CTA kuat weekend"),
    ("2026-11-17", "IG Carousel 5 Angka Digital 2027", "5 Angka Laporan Baru yang Menentukan Bisnismu 2027", "Instagram Carousel", "Digital 2027", "data segar, awal minggu B2B"),
    ("2026-11-19", "TikTok 240 Juta Peluang atau Jebakan", "TikTok 240 Juta Pengguna: Peluang atau Jebakan?", "TikTok", "Digital 2027", "jaga ritme TikTok"),
    ("2026-11-20", "IG Reels Digital Marketing Bukan Konten Viral", "Digital Marketing Itu Bukan Konten Viral", "Instagram Reels", "UMKM Kalsel", "tutup 2 minggu dengan positioning lokal"),
]
with open("data/jadwal_posting.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=HJ); w.writeheader(); w.writerows([dict(zip(HJ, r)) for r in jadwal])
print(f"jadwal_posting.csv: {len(jadwal)} entri")

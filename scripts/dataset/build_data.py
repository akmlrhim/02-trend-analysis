# -*- coding: utf-8 -*-
"""Membangun CSV dataset tren dari data mentah yang terkumpul. Tanggal ambil: 2026-11-06."""
import csv, json, os

TGL = "2026-11-06"
os.makedirs("data", exist_ok=True)

def w(path, header, rows):
    # validasi: buang duplikat berdasarkan kolom kunci pertama yang cocok
    seen, out = set(), []
    for r in rows:
        if not isinstance(r, dict):
            r = dict(zip(header, r))
        key = "|".join(str(r.get(h, "")).strip().lower() for h in header[:3])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=header)
        wr.writeheader()
        for r in out:
            wr.writerow({h: r.get(h, "") for h in header})
    print(f"{path}: {len(out)} baris (dari {len(rows)})")

# ============ DATASET 1: tren_topik.csv ============
H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
D1 = []
URL_RSS = "https://trends.google.com/trending/rss?geo=ID"

# 1a. Google Trends - Trending now (RSS geo=ID)
rss = [
    ("Perlinsos Kemensos login digital", "perlinsos kemensos go id login", "layanan_publik", "500+", "netral"),
    ("Indeks Kospi Korea anjlok", "kospi index", "finansial_global", "100+", "negatif"),
    ("Uji kompetensi ASN digital BKN", "asn digital bkn", "layanan_publik", "200+", "netral"),
    ("Polres Metro Jakarta Pusat / konser Andrea Bocelli", "polres metro jakarta pusat", "keamanan_hiburan", "200+", "netral"),
    ("Helikopter TNI Mi-17 jatuh di Kalteng", "mil mi-17", "berita_nasional", "200+", "negatif"),
    ("Cruzeiro vs Bahia", "cruzeiro vs bahia", "olahraga_internasional", "1000+", "netral"),
    ("Kospi hentikan perdagangan sementara", "kospi", "finansial_global", "500+", "negatif"),
    ("Sidang Samin Tan tambang ilegal", "pt. asmin koalindo tuhup", "hukum_energi", "100+", "negatif"),
    ("Kasus penyadapan / evaluasi polri", "cek", "berita_nasional", "500+", "negatif"),
    ("Persib menang di Melbourne (ACL Two)", "liga champions asia", "olahraga_nasional", "1000+", "positif"),
]
for topik, kw, kat, vol, sen in rss:
    D1.append({"kategori": kat, "topik": topik, "kata_kunci": kw, "sumber": "Google Trends - Trending Now (RSS, geo=ID)",
               "indikator_tren": "naik", "skor_atau_volume": vol, "sentimen": sen, "source_url": URL_RSS})

# 1b. Google Trends - Interest over time 12 bulan (pytrends)
iot = [
    ("belanja online", "e_commerce", 5.1, 5, 6, "naik"),
    ("resep masakan", "kuliner", 7.2, 8, 7, "stabil"),
    ("liburan", "travel", 31.7, 23, 28, "naik"),
    ("smartphone", "teknologi", 16.5, 18, 11, "turun"),
    ("skincare", "kecantikan", 79.2, 75, 78, "naik"),
    ("viral", "media_sosial", 55.9, 41, 39, "turun"),
    ("kripto", "finansial", 1.0, 1, 1, "stabil"),
    ("lowongan kerja", "karier", 6.7, 7, 7, "stabil"),
    ("olahraga", "gaya_hidup", 19.0, 19, 20, "stabil"),
    ("film indonesia", "hiburan", 10.7, 13, 8, "turun"),
]
for kw, kat, avg, first, last, ind in iot:
    D1.append({"kategori": kat, "topik": f"Interest over time 12 bulan: {kw}", "kata_kunci": kw,
               "sumber": "Google Trends - Interest Over Time 12 bulan (pytrends)",
               "indikator_tren": ind, "skor_atau_volume": f"avg={int(avg)}, awal={first}, akhir={last}",
               "sentimen": "netral", "source_url": f"https://trends.google.com/trends/explore?geo=ID&q={kw.replace(' ', '%20')}"})

# 1c. Google Trends - Related queries (Rising & Top)
rq = [
    ("belanja online", "e_commerce", "rising", "aplikasi belanja online murah", "60%"),
    ("belanja online", "e_commerce", "rising", "astro belanja online", "60%"),
    ("belanja online", "e_commerce", "top", "cara belanja online", "100"),
    ("belanja online", "e_commerce", "top", "aplikasi belanja online", "95"),
    ("belanja online", "e_commerce", "top", "shopee belanja online", "60"),
    ("belanja online", "e_commerce", "top", "belanja online murah", "28"),
    ("belanja online", "e_commerce", "top", "indomaret belanja online", "21"),
    ("resep masakan", "kuliner", "rising", "resep masakan mcgg", "23100%"),
    ("resep masakan", "kuliner", "rising", "resep rica rica ayam masakan jawa", "100%"),
    ("resep masakan", "kuliner", "top", "resep masakan ayam", "100"),
    ("resep masakan", "kuliner", "top", "resep masakan ikan", "61"),
    ("resep masakan", "kuliner", "top", "resep masakan sehari hari", "46"),
    ("liburan", "travel", "top", "liburan sekolah", "100"),
    ("liburan", "travel", "top", "liburan 2026", "56"),
    ("liburan", "travel", "top", "tempat liburan", "51"),
    ("liburan", "travel", "top", "liburan keluarga", "43"),
    ("smartphone", "teknologi", "rising", "best smartphone 2026", "11700%"),
    ("smartphone", "teknologi", "rising", "foldable smartphone", "400%"),
    ("smartphone", "teknologi", "top", "smartphone samsung", "100"),
    ("smartphone", "teknologi", "top", "harga smartphone", "82"),
    ("smartphone", "teknologi", "top", "smartphone 5g", "44"),
    ("skincare", "kecantikan", "rising", "kime skincare", "500%"),
    ("skincare", "kecantikan", "rising", "drve skincare", "350%"),
    ("skincare", "kecantikan", "rising", "basic skincare dr tompi", "200%"),
    ("skincare", "kecantikan", "top", "urutan skincare", "100"),
    ("skincare", "kecantikan", "top", "produk skincare", "96"),
    ("skincare", "kecantikan", "top", "skincare bpom", "66"),
    ("skincare", "kecantikan", "top", "sunscreen", "57"),
    ("viral", "media_sosial", "rising", "teh pucuk viral", "38250%"),
    ("viral", "media_sosial", "rising", "inara rusli viral", "28950%"),
    ("viral", "media_sosial", "rising", "lagu viral tiktok 2026", "26550%"),
    ("viral", "media_sosial", "rising", "guru bahasa inggris viral", "9000%"),
    ("viral", "media_sosial", "top", "indo viral", "100"),
    ("viral", "media_sosial", "top", "lagu viral", "26"),
    ("kripto", "finansial", "rising", "pt pedagang aset kripto", "400%"),
    ("kripto", "finansial", "top", "uang kripto", "100"),
    ("kripto", "finansial", "top", "harga kripto", "77"),
    ("kripto", "finansial", "top", "kripto indonesia", "75"),
    ("lowongan kerja", "karier", "rising", "lowongan kerja 2026", "6350%"),
    ("lowongan kerja", "karier", "rising", "lowongan kerja mbg terdekat", "3350%"),
    ("lowongan kerja", "karier", "rising", "lowongan kerja bumn 2026", "1800%"),
    ("lowongan kerja", "karier", "rising", "cpns 2026", "1650%"),
    ("lowongan kerja", "karier", "top", "lowongan kerja 2026", "100"),
    ("lowongan kerja", "karier", "top", "loker", "86"),
    ("lowongan kerja", "karier", "top", "lowongan kerja jakarta", "81"),
    ("olahraga", "gaya_hidup", "rising", "malaysia vs singapura", "5950%"),
    ("olahraga", "gaya_hidup", "rising", "olahraga hyrox", "1050%"),
    ("olahraga", "gaya_hidup", "top", "baju olahraga", "57"),
    ("olahraga", "gaya_hidup", "top", "manfaat olahraga", "40"),
    ("film indonesia", "hiburan", "rising", "film horor indonesia 2026", "11650%"),
    ("film indonesia", "hiburan", "rising", "film indonesia 2026", "6550%"),
    ("film indonesia", "hiburan", "rising", "agak laen 2", "1350%"),
    ("film indonesia", "hiburan", "top", "film horor indonesia", "100"),
    ("film indonesia", "hiburan", "top", "film indonesia terbaru", "84"),
]
for kw, kat, jenis, q, val in rq:
    D1.append({"kategori": kat, "topik": f"Related query {jenis.upper()}: {q}", "kata_kunci": kw,
               "sumber": f"Google Trends - Related Queries ({jenis})",
               "indikator_tren": "naik" if jenis == "rising" else "stabil", "skor_atau_volume": val,
               "sentimen": "netral", "source_url": f"https://trends.google.com/trends/explore?geo=ID&q={kw.replace(' ', '%20')}"})

# 1d. Interest by region (provinsi)
ibr = [
    ("belanja online", "Gorontalo 100, Banten 96, Kalimantan Tengah 94, Sumatera Barat 89, Riau 88"),
    ("resep masakan", "Jawa Tengah 100, Jawa Timur 88, DIY 86, Kalimantan Tengah 76"),
    ("liburan", "Jawa Tengah 100, Jawa Timur 99, Banten 86, DIY 82"),
    ("smartphone", "Sumatera Barat 100, DKI Jakarta 85, DIY 69, Bali 63"),
    ("skincare", "Jawa Tengah 100, Jawa Timur 89, Sulawesi Selatan 80, Lampung 78"),
]
for kw, prov in ibr:
    D1.append({"kategori": "geolokasi", "topik": f"Interest by region: {kw}", "kata_kunci": f"{kw} | provinsi teratas: {prov}",
               "sumber": "Google Trends - Interest by Region (pytrends, resolusi provinsi)",
               "indikator_tren": "stabil", "skor_atau_volume": "skala 0-100", "sentimen": "netral",
               "source_url": f"https://trends.google.com/trends/explore?geo=ID&q={kw.replace(' ', '%20')}"})

# 1e. X/Twitter trending via agregator
xt = ["#TikTokShopBerbagiRatusanJuta", "75th Humas Mengabdi", "Trip", "#DewTeeFanconLIVE",
      "#SANTA23rdSilverBurst", "Jokowi", "SANTA 23RD GLEAMING", "PERTHSANTA MEMORABLE NIGHT",
      "#savepresiden", "#iQIYIiJOYTH2027xDMD", "DEWTEE SECRET AREA LIVE", "iPhone 18 Pro Max",
      "Hadiah Ratusan Juta", "Roy Suryo", "Tailor", "transparansi tanpa tebang pilih",
      "wujudkan pembangunan bersama", "sumber daya manusia unggul", "WOULD YOU TAKE MY RING"]
for t in xt:
    sen = "negatif" if ("Roy Suryo" in t or "savepresiden" in t) else "netral"
    D1.append({"kategori": "media_sosial", "topik": f"X trending: {t}", "kata_kunci": t,
               "sumber": "X (Twitter) Trending via agregator lagitren.id",
               "indikator_tren": "naik", "skor_atau_volume": "", "sentimen": sen,
               "source_url": "https://lagitren.id/twitter"})

# 1f. Berita (Google News RSS)
news = [
    ("Penyadapan ilegal: tersangka baru Slamet Uliandi", "hukum", "detikNews", "negatif"),
    ("MA: suket ijazah SMA Gibran tak sah, Jokowi merespons", "politik", "detikNews", "negatif"),
    ("Pramono bantah kabar Jakarta Siaga 1", "politik_keamanan", "detikNews", "netral"),
    ("Trump kalah telak di pemilu sela AS", "politik_internasional", "CNBC Indonesia", "netral"),
    ("Presiden Paraguay Santiago Pena mundur", "politik_internasional", "detikNews", "negatif"),
    ("Ekonomi RI tumbuh 5,47% YoY Q3 2026", "ekonomi", "Stockbit Snips", "positif"),
    ("Harga Bitcoin tembus US$80.000", "finansial", "detikFinance", "positif"),
    ("Pengangguran turun meski banyak PHK (BPS)", "ekonomi", "detikFinance", "positif"),
    ("Peluang pasar modal RI lolos standalone market MSCI tipis", "finansial", "Kompas.com", "negatif"),
    ("Kacamata Meta masuk RI, isu privasi", "teknologi", "CNBC Indonesia", "negatif"),
    ("Jadwal rilis HyperOS 4 untuk Xiaomi/Redmi/Poco", "teknologi", "Kompas.com", "netral"),
    ("WhatsApp: foto galeri langsung muncul di ruang chat", "teknologi", "Tribunnews.com", "netral"),
    ("3 prajurit TNI gugur usai helikopter jatuh (karhutla)", "berita_nasional", "detikNews", "negatif"),
    ("Komnas HAM tinjau pelanggaran HAM polisi di Sukoharjo", "hukum_HAM", "Tirto.id", "negatif"),
    ("Satelit NASA 1,4 ton jatuh di Sumatera", "sains", "DW.com", "netral"),
    ("Temuan sel darah dinosaurus di fosil", "sains", "detikInet", "netral"),
    ("Aktivitas vulkanik Mars belum mati", "sains", "Media Indonesia", "netral"),
    ("AS sumbang 50 unit rontgen portabel untuk TBC", "kesehatan", "MOST 1058", "positif"),
    ("Fanny Ghassani hamil usai penantian 9 tahun", "hiburan", "detikHOT", "positif"),
    ("Audi Marissa dan Anthony Xie sepakati perceraian", "hiburan", "okezone", "netral"),
    ("Marc Marquez balapan di MotoGP Qatar 2026", "olahraga", "CNN Indonesia", "netral"),
    ("AZ Alkmaar vs Juventus 2-1 di Liga Champions", "olahraga", "detikSport", "netral"),
    ("Como 1-9: kemenangan bersejarah Belanda", "olahraga", "Goal.com", "netral"),
    ("Meme dan jokes jadul masih kocak", "internet_budaya", "detikInet", "netral"),
    ("Satu Data Indonesia: urusan dokumen tak bolak-balik", "layanan_publik", "detikInet", "positif"),
    ("Kospi Korea anjlok 8,6%, Samsung/SK Hynix terjun bebas", "finansial_global", "investing.com", "negatif"),
]
for topik, kat, media, sen in news:
    D1.append({"kategori": kat, "topik": topik, "kata_kunci": "", "sumber": f"Berita via Google News RSS ({media})",
               "indikator_tren": "naik", "skor_atau_volume": "", "sentimen": sen,
               "source_url": "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id"})

# 1g. TikTok trending
tt = [
    ("Behind the scenes (@mega)", "56246473", "netral"),
    ("Hoobah (@Jennifer Hubner)", "28110743", "netral"),
    ("TikTok video (@Shabrinaadfi)", "22753209", "netral"),
    ("Konten meme 🗿 (@Hansen Vendi Agus)", "12928009", "netral"),
    ("Macet di lintas Sumatera, #driverkampus", "12742640", "netral"),
    ("#rakserbaguna (@Silvia)", "9418226", "netral"),
    ("Balik kampung (@lalilaa.m)", "8248024", "netral"),
    ("#ceocimol (@CEO CIMOL)", "8120178", "netral"),
    ("#gehalda couple prank (@Geha n Alda)", "1354747", "netral"),
]
for topik, views, sen in tt:
    D1.append({"kategori": "media_sosial", "topik": f"TikTok trending: {topik}", "kata_kunci": "#fyp #trending",
               "sumber": "TikTok trending via agregator socialmediadefined.com (TikTok Creative Center API gagal)",
               "indikator_tren": "naik", "skor_atau_volume": f"views={views}", "sentimen": sen,
               "source_url": "https://socialmediadefined.com/id/trending"})
D1.append({"kategori": "media_sosial", "topik": "Hashtag TikTok naik: #driverkampus, #ceocimol, #rakserbaguna, #gehalda, #coupleprank, #fyp",
           "kata_kunci": "driverkampus; ceocimol; rakserbaguna; gehalda; fyp", "sumber": "TikTok trending via agregator socialmediadefined.com",
           "indikator_tren": "naik", "skor_atau_volume": "", "sentimen": "netral",
           "source_url": "https://socialmediadefined.com/id/trending"})

# 1h. YouTube trending
yt = [
    ("TREASURE - 'SHOCK' M/V (rank #1, HYBE LABELS)", "views=13000000", "netral"),
    ("TERIKAT JANJI trailer (Arya Saloka, Asha)", "", "netral"),
    ("NOAH - Hidup Untukmu, Mati Tanpamu (Official 4K MV)", "views=49000", "positif"),
    ("Pasukan SAKADUNG APPLE - Halo Budi (kreator kecil 316K sub naik daftar)", "views=134000", "netral"),
    ("Lagu santai viral TikTok 2026 - Top Hits Indonesia (youtrendings)", "", "netral"),
]
for topik, views, sen in yt:
    D1.append({"kategori": "hiburan", "topik": f"YouTube trending ID: {topik}", "kata_kunci": "trending youtube indonesia",
               "sumber": "YouTube trending via agregator CreatorDB / youtrendings.com",
               "indikator_tren": "naik", "skor_atau_volume": views, "sentimen": sen,
               "source_url": "https://creatordb.app/free-tools/whats-trending-on-youtube/indonesia"})

# 1i. Marketplace / e-commerce
D1.append({"kategori": "e_commerce", "topik": "Kategori terlaris marketplace: elektronik, gadget, fashion", "kata_kunci": "elektronik; gadget; fashion",
           "sumber": "Marketplace via artikel analisis (accio.com, Tokopedia blog)",
           "indikator_tren": "stabil", "skor_atau_volume": "", "sentimen": "netral",
           "source_url": "https://www.accio.com/business/id/produk-tokopedia-terlaris"})
D1.append({"kategori": "e_commerce", "topik": "Live shopping / social commerce TikTok Shop naik", "kata_kunci": "live shopping; tiktok shop",
           "sumber": "Marketplace via artikel analisis (accio.com)",
           "indikator_tren": "naik", "skor_atau_volume": "", "sentimen": "netral",
           "source_url": "https://www.accio.com/business/id/produk-tokopedia-terlaris"})
D1.append({"kategori": "e_commerce", "topik": "Produk ramah lingkungan & refill naik", "kata_kunci": "eco friendly; kemasan biodegradable; refill",
           "sumber": "Marketplace via artikel analisis (accio.com)",
           "indikator_tren": "naik", "skor_atau_volume": "", "sentimen": "netral",
           "source_url": "https://www.accio.com/business/id/produk-tokopedia-terlaris"})

# 1j. Instagram via agregator hashtag
D1.append({"kategori": "media_sosial", "topik": "Hashtag IG volume besar (global): #indonesia, #trending, #explore",
           "kata_kunci": "#indonesia 318.2M posts; #trending 902.4M; #explore 794M",
           "sumber": "Instagram via agregator iqhashtags (data global, bukan khusus ID)",
           "indikator_tren": "stabil", "skor_atau_volume": "posts=318200000", "sentimen": "netral",
           "source_url": "https://iqhashtags.com/hashtags/hashtag/indonesia"})
D1.append({"kategori": "media_sosial", "topik": "Kategori Reels IG naik Nov 2026 (global): interior & home decor",
           "kata_kunci": "#interiordesign 26.7K; #homedecor 17K (Okt 2-31 2026)",
           "sumber": "Instagram via agregator Dash Social (data global)",
           "indikator_tren": "naik", "skor_atau_volume": "posts=26700", "sentimen": "netral",
           "source_url": "https://www.dashsocial.com/blog/instagram-hashtags"})

w("data/tren_topik.csv", H1, D1)

# ============ DATASET 2: pertanyaan_audiens.csv ============
H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]
D2 = []
UA = "https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=ID&q="

ac1 = [
    ("kesehatan", "kenapa sering buang air kecil"), ("kesehatan", "kenapa kepala sering pusing"),
    ("kesehatan", "kenapa mata kiri berkedut terus"), ("kesehatan", "kenapa perut bagian bawah sakit"),
    ("kesehatan", "kenapa bab keluar darah"), ("kesehatan", "kenapa payudara terasa nyeri"),
    ("kesehatan", "kenapa telinga berdenging sebelah"),
    ("politik", "kenapa jokowi di sidang"), ("politik", "kenapa roy suryo mempermasalahkan ijazah jokowi"),
    ("umum", "apa itu makar"), ("umum", "apa itu desil"), ("psikologi", "apa itu npd"),
    ("lingkungan", "apa itu karhutla"), ("politik", "apa itu senator amerika"),
    ("kesehatan", "apa itu hiv"), ("kuliner", "apa itu kimpul"), ("ekonomi", "apa itu oligarki"),
    ("pajak", "apa itu npwp"),
    ("umum", "bagaimana cara menghindari dampak negatif dari globalisasi"),
    ("umum", "bagaimana cara mengecek desil kita"),
    ("keamanan_digital", "bagaimana cara mengetahui dan mencegah penyadapan hp"),
    ("keagamaan", "berapa hari lagi puasa 2027"), ("keagamaan", "berapa bulan lagi puasa 2027"),
    ("keagamaan", "berapa hari lagi ramadhan 2027"), ("kuliner", "berapa menit merebus telur"),
    ("adm_dokumen", "cara membuat npwp online"), ("produktivitas", "cara membuat google form"),
    ("karier", "cara membuat cv lamaran kerja"), ("adm_dokumen", "cara membuat email baru"),
    ("adm_dokumen", "cara membuat npwp"), ("produktivitas", "cara membuat daftar isi otomatis di word"),
    ("kuliner", "cara membuat asinan mangga"), ("produktivitas", "cara membuat akun google baru"),
]
ac2 = [
    ("teknologi", "kenapa hp cepat panas"), ("teknologi", "kenapa hp tidak bisa di cas"),
    ("teknologi", "kenapa hp bisa mati sendiri"), ("teknologi", "kenapa hp tiba tiba mati"),
    ("teknologi", "kenapa hp sering panas"), ("teknologi", "kenapa hp ada iklan terus"),
    ("teknologi", "kenapa hp iphone tiba tiba mati sendiri"),
    ("energi", "kenapa listrik sering mati"), ("energi", "kenapa listrik mati hidup mati hidup"),
    ("energi", "kenapa listrik mati sendiri padahal token masih ada"),
    ("energi", "kenapa listrik di kalsel mati"), ("energi", "kenapa listrik sering padam"),
    ("regulasi", "apa itu bpom ri"), ("regulasi", "apa itu bpom makanan"),
    ("regulasi", "apa itu bpom skincare"), ("regulasi", "apa itu bpom md"),
    ("regulasi", "apa itu bpom dalam bahasa gaul"),
    ("keamanan", "di mana kebakaran hari ini"), ("kesehatan", "di mana letak ginjal"),
    ("sejarah", "di mana tempat pembacaan teks proklamasi"),
    ("kalender", "kapan hari guru"), ("kalender", "kapan bulan puasa 2027"),
    ("cuaca", "kapan musim hujan 2026"), ("cuaca", "kapan hujan di kalimantan selatan"),
    ("kalender", "kapan hari ayah"),
    ("otomotif_bbm", "berapa harga pertamax sekarang"), ("teknologi", "berapa harga iphone 17 pro max"),
    ("finansial", "berapa harga dolar hari ini"), ("finansial", "berapa harga emas hari ini"),
    ("teknologi", "berapa harga iphone 13"), ("teknologi", "berapa harga iphone 18 pro max"),
    ("bansos", "cara daftar perlinsos"), ("pajak", "cara daftar npwp online"),
    ("bansos", "cara daftar ikd"), ("gig_ekonomi", "cara daftar driver shopee food"),
    ("kesehatan", "cara daftar jkn mobile"), ("gig_ekonomi", "cara daftar shopee affiliate"),
    ("energi", "cara daftar barcode pertamina online"),
    ("telekomunikasi", "cara cek nomor telkomsel"), ("telekomunikasi", "cara cek nomor indosat"),
    ("telekomunikasi", "cara cek kuota telkomsel"), ("perbankan", "cara cek bi checking"),
    ("bansos", "cara cek bsu"), ("telekomunikasi", "cara cek nomor im3"),
    ("perbankan", "cara cek slik ojk"), ("pajak", "cara cek npwp pakai nik"),
    ("bansos", "cara cek bansos"),
    ("pajak", "cara download npwp di coretax"), ("media_sosial", "cara download video tiktok hd"),
    ("teknologi", "cara download video youtube di komputer"), ("teknologi", "cara download wa di laptop"),
    ("internet", "kenapa internet tidak bisa digunakan padahal kuota masih ada"),
    ("internet", "kenapa internet lemot"), ("internet", "kenapa internet indonesia lemot"),
    ("internet", "kenapa internet telkomsel lemot"), ("internet", "kenapa internet wifi tidak tersedia"),
    ("internet", "kenapa internet rakyat sering gangguan"),
    ("ekonomi", "kenapa harga hp naik"), ("finansial", "kenapa harga emas turun"),
    ("teknologi", "kenapa harga ram naik"), ("ekonomi", "kenapa harga hp sekarang mahal"),
    ("finansial", "kenapa harga emas naik"), ("transportasi", "kenapa harga tiket pesawat mahal"),
    ("teknologi", "kenapa harga laptop naik"),
    ("pembayaran_digital", "cara top up shopeepay"), ("pembayaran_digital", "cara top up dana"),
    ("perbankan", "cara top up seabank"), ("perbankan", "cara top up dana dari bca"),
    ("gaming", "cara top up robux"), ("pembayaran_digital", "cara top up gopay"),
    ("asuransi", "apa itu denda ritl bpjs"), ("otomotif", "apa itu denda swdkllj"),
    ("otomotif", "apa itu denda pkb"), ("keagamaan", "apa itu denda kafarat"),
    ("otomotif", "apa itu denda opsen pkb"),
    ("perbankan", "cara transfer bca ke dana"), ("telekomunikasi", "cara transfer pulsa telkomsel"),
    ("pembayaran_digital", "cara transfer gopay ke dana"), ("pembayaran_digital", "cara transfer ovo ke dana"),
    ("telekomunikasi", "cara transfer kuota im3"), ("perbankan", "cara transfer dana dari bca"),
    ("kepegawaian", "cara klaim jht online"), ("kepegawaian", "cara klaim jkp"),
    ("kepegawaian", "cara klaim bpjs ketenagakerjaan online"), ("kepegawaian", "cara klaim jkp bulan ke 2"),
    ("bansos", "cara klaim bsu"),
    ("karier", "berapa gaji tni"), ("karier", "berapa gaji kepala desa perbulan"),
    ("karier", "berapa gaji alfamart"), ("karier", "berapa gaji indomaret"),
    ("karier", "berapa gaji satpam"), ("karier", "berapa gaji kurir spx"),
]
for kat, q in ac1 + ac2:
    D2.append({"kategori": kat, "pertanyaan_atau_keluhan": q, "sumber": "Google autocomplete (suggest API, hl=id gl=ID)",
               "frekuensi_atau_jumlah_mention": "", "source_url": UA + q.replace(" ", "%20")})

# Trends related queries berbentuk pertanyaan / 'cara'
trq = [
    ("e_commerce", "cara belanja online", "100"), ("e_commerce", "aplikasi belanja online", "95"),
    ("teknologi", "smartphone adalah", "81"), ("teknologi", "harga smartphone", "82"),
    ("kecantikan", "urutan skincare", "100"), ("kecantikan", "harga skincare", "68"),
    ("kecantikan", "kandungan skincare", "54"), ("kecantikan", "basic skincare", "49"),
    ("gaya_hidup", "manfaat olahraga", "40"), ("gaya_hidup", "apa itu olahraga", "29"),
    ("finansial", "kripto adalah", "67"), ("finansial", "harga kripto", "77"),
    ("finansial", "kripto hari ini", "50"), ("karier", "info lowongan kerja", "39"),
    ("karier", "lowongan kerja terbaru", "44"), ("travel", "liburan adalah", "35"),
    ("travel", "kata kata liburan", "31"), ("hiburan", "rekomendasi film indonesia", "22"),
    ("kecantikan", "skincare yang aman untuk ibu hamil", ""), ("kecantikan", "skincare yang cepat memutihkan", ""),
    ("kecantikan", "skincare yang bagus", ""),
]
for kat, q, val in trq:
    D2.append({"kategori": kat, "pertanyaan_atau_keluhan": q, "sumber": "Google Trends - Related Queries (Top/Rising)",
               "frekuensi_atau_jumlah_mention": val, "source_url": "https://trends.google.com/trends/explore?geo=ID"})

# Reddit via tavily
red = [
    ("media_sosial", "Kenapa scene podcast di Indonesia ramai dan terus berkembang?"),
    ("teknologi", "Apakah situs Coretax aman? Ramai soal situs Coretax tak dilengkapi keamanan API"),
    ("politik", "Mengapa konten demo mahasiswa yang lama ramai lagi di medsos?"),
    ("migrasi", "Bagaimana cara pindah ke Australia?"),
    ("media_sosial", "Apakah Reddit clone versi lokal bisa dibuat di Indonesia?"),
]
for kat, q in red:
    D2.append({"kategori": kat, "pertanyaan_atau_keluhan": q, "sumber": "Reddit r/indonesia (via pencarian tavily; API langsung diblokir 403)",
               "frekuensi_atau_jumlah_mention": "", "source_url": "https://www.reddit.com/r/indonesia/"})

# Kaskus via tavily
kas = [
    ("olahraga", "Diskusi timnas Indonesia road to World Cup 2026"),
    ("teknologi", "Thread komparasi dan konsultasi sebelum membeli perangkat elektronik"),
]
for kat, q in kas:
    D2.append({"kategori": kat, "pertanyaan_atau_keluhan": q, "sumber": "Kaskus (via pencarian tavily; halaman utama SPA/JS)",
               "frekuensi_atau_jumlah_mention": "", "source_url": "https://www.kaskus.co.id/"})

w("data/pertanyaan_audiens.csv", H2, D2)

# ============ DATASET 5: kalender_momen.csv ============
H5 = ["tanggal", "nama_momen", "jenis", "relevansi", "catatan", "source_url"]
D5 = [
    ("2026-11-07", "Hari Wayang Nasional", "hari_besar", "rendah", "Peringatan nasional non-libur", "https://www.kompas.tv/info-publik/697695/daftar-hari-nasional-november-2026-apakah-ada-libur-tanggal-merah"),
    ("2026-11-10", "Hari Pahlawan", "hari_besar", "tinggi", "Peringatan nasional, bukan libur; momen konten patriotik", "https://www.kompas.tv/info-publik/697695/daftar-hari-nasional-november-2026-apakah-ada-libur-tanggal-merah"),
    ("2026-11-10", "Gajian awal bulan (periode pertengahan)", "gajian", "sedang", "Sebagian perusahaan membayar gaji tanggal 10", "https://www.bigseller.com/blog/articleDetails/jadwal-promo-ecommerce.4080.htm"),
    ("2026-11-11", "Promo 11.11 / tanggal kembar November", "musim_belanja", "tinggi", "Kampanye besar marketplace pembuka musim belanja akhir tahun", "https://tokoprogress.com/2026/10/20/tips-memaksimalkan-promo-11-11-dan-12-12-untuk-beli-kulkas-panduan-anti-rugi"),
    ("2026-11-11", "Hari Bangunan Indonesia", "hari_besar", "rendah", "Peringatan nasional non-libur", "https://www.kompas.tv/info-publik/697695/daftar-hari-nasional-november-2026-apakah-ada-libur-tanggal-merah"),
    ("2026-11-12", "Hari Kesehatan Nasional", "hari_besar", "sedang", "Peringatan nasional non-libur", "https://www.suara.com/news/2026/11/02/182217/apakah-bulan-november-2026-ada-tanggal-merah-ini-daftar-hari-libur-sesuai-skb-3-menteri"),
    ("2026-11-12", "Hari Ayah Nasional", "hari_besar", "sedang", "Momen konten keluarga", "https://www.suara.com/news/2026/11/02/182217/apakah-bulan-november-2026-ada-tanggal-merah-ini-daftar-hari-libur-sesuai-skb-3-menteri"),
    ("2026-11-14", "Hari Diabetes Sedunia", "hari_besar", "sedang", "Hari internasional kesehatan", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-11-15", "Borobudur Marathon 2026", "event_industri", "sedang", "Magelang, Jawa Tengah", "https://www.cnbcindonesia.com/news/20260726161747-4-753877/indonesia-jadi-tuan-rumah-event-dunia-2026-2027-cek-daftarnya"),
    ("2026-11-19", "Hari Toilet Sedunia", "hari_besar", "rendah", "Hari internasional", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-11-20", "Hari Anak Sedunia", "hari_besar", "sedang", "Universal Children's Day", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-11-20", "GAIKINDO Jakarta Auto Week (GJAW) 2026", "event_industri", "sedang", "20-29 Nov, ICE BSD City", "https://printpoin.com/blog/jadwal-pameran-ice-bsd-november-desember-2026"),
    ("2026-11-20", "Indonesia Motorcycle Show (IMOS) 2026", "event_industri", "sedang", "20-29 Nov, ICE BSD City", "https://printpoin.com/blog/jadwal-pameran-ice-bsd-november-desember-2026"),
    ("2026-11-22", "Hari Perhubungan Darat Nasional", "hari_besar", "rendah", "Peringatan nasional non-libur", "https://www.suara.com/news/2026/11/02/182217/apakah-bulan-november-2026-ada-tanggal-merah-ini-daftar-hari-libur-sesuai-skb-3-menteri"),
    ("2026-11-25", "Hari Guru Nasional", "hari_besar", "tinggi", "Peringatan nasional non-libur; momen konten apresiasi guru", "https://www.kompas.tv/info-publik/697695/daftar-hari-nasional-november-2026-apakah-ada-libur-tanggal-merah"),
    ("2026-11-25", "Gajian akhir bulan", "gajian", "tinggi", "Momen belanja setelah gajian", "https://www.bigseller.com/blog/articleDetails/jadwal-promo-ecommerce.4080.htm"),
    ("2026-11-25", "Decoration & Furniture Indonesia 2026", "event_industri", "rendah", "25-28 Nov, NICE (Jakarta International Expo tercantum di exposale)", "https://exposale.net/id/exhibitions/all/all/126"),
    ("2026-11-26", "Jakarta Pet Expo 2026", "event_industri", "rendah", "26-28 Nov, JIExpo Kemayoran", "https://exposale.net/id/exhibitions/all/all/126"),
    ("2026-11-27", "Black Friday 2026", "musim_belanja", "tinggi", "Jumat 27 Nov 2026; kampanye diskon global yang diadopsi e-commerce RI", "https://www.shopperqueries.com/blog/kalender-promo-online"),
    ("2026-11-27", "Simple Plan Indonesia Tour", "event_industri", "sedang", "27 Nov Jakarta, 28 Nov Surabaya", "https://www.cnbcindonesia.com/news/20260726161747-4-753877/indonesia-jadi-tuan-rumah-event-dunia-2026-2027-cek-daftarnya"),
    ("2026-11-28", "Joyland Sessions 2026", "event_industri", "sedang", "Festival musik 28-29 Nov", "https://www.cnbcindonesia.com/news/20260726161747-4-753877/indonesia-jadi-tuan-rumah-event-dunia-2026-2027-cek-daftarnya"),
    ("2026-11-30", "Cyber Monday 2026", "musim_belanja", "sedang", "Senin setelah Black Friday", "https://www.shopperqueries.com/blog/kalender-promo-online"),
    ("2026-12-01", "Hari AIDS Sedunia", "hari_besar", "sedang", "Hari internasional kesehatan", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-12-01", "Gajian awal Desember", "gajian", "sedang", "Momen belanja awal bulan", "https://www.bigseller.com/blog/articleDetails/jadwal-promo-ecommerce.4080.htm"),
    ("2026-12-03", "Hari Disabilitas Internasional", "hari_besar", "sedang", "Hari internasional inklusi", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-12-03", "INDOVEC EXPO 2026", "event_industri", "rendah", "Pameran ke-13, 3-6 Des, Nagoya Hill Batam", "https://jadwalevent.web.id"),
    ("2026-12-10", "Hari HAM Sedunia", "hari_besar", "tinggi", "Hari internasional besar", "https://www.metrotvnews.com/read/N9nCdO0o-daftar-hari-besar-nasional-dan-internasional-november-2026"),
    ("2026-12-10", "Gajian tengah bulan", "gajian", "sedang", "Sebagian perusahaan membayar tanggal 10", "https://www.bigseller.com/blog/articleDetails/jadwal-promo-ecommerce.4080.htm"),
    ("2026-12-12", "Harbolnas 12.12 / Hari Belanja Online Nasional", "musim_belanja", "tinggi", "12 Des bertepatan Hari Belanja Online Nasional (Harbolnas)", "https://tokoprogress.com/2026/10/20/tips-memaksimalkan-promo-11-11-dan-12-12-untuk-beli-kulkas-panduan-anti-rugi"),
    ("2026-12-15", "IESF World Esports Championship (WEC26)", "event_industri", "sedang", "15-20 Des, ICE BSD City", "https://printpoin.com/blog/jadwal-pameran-ice-bsd-november-desember-2026"),
    ("2026-12-22", "Hari Ibu", "hari_besar", "tinggi", "Peringatan nasional non-libur; momen konten keluarga besar", "https://www.kompas.tv/info-publik/697695/daftar-hari-nasional-november-2026-apakah-ada-libur-tanggal-merah"),
    ("2026-12-24", "Cuti Bersama Hari Raya Natal", "libur_nasional", "tinggi", "Cuti bersama resmi SKB; awal libur panjang 24-27 Des", "https://kalenderku.id"),
    ("2026-12-25", "Hari Raya Natal", "libur_nasional", "tinggi", "Libur nasional resmi (17 libur nasional 2026)", "https://kalenderku.id"),
    ("2026-12-25", "Gajian akhir Desember + Natal", "gajian", "tinggi", "Gajian akhir tahun bertepatan musim Natal", "https://www.bigseller.com/blog/articleDetails/jadwal-promo-ecommerce.4080.htm"),
    ("2026-12-31", "Malam Tahun Baru", "hari_besar", "tinggi", "Momen perayaan & promosi tutup tahun", "https://kalenderku.id"),
    ("2027-01-01", "Tahun Baru Masehi 2027", "libur_nasional", "tinggi", "Libur nasional; long weekend 1-3 Jan", "https://hari.co.id/libur-nasional/2027"),
    ("2027-01-01", "Promo Tahun Baru / clearances akhir tahun", "musim_belanja", "sedang", "Kampanye new year sale e-commerce", "https://www.shopperqueries.com/blog/kalender-promo-online"),
    ("2027-01-04", "Cuti Bersama Isra Mikraj Nabi Muhammad SAW", "libur_nasional", "sedang", "Cuti bersama resmi SKB 2027", "https://hari.co.id/libur-nasional/2027"),
    ("2027-01-05", "Isra Mikraj Nabi Muhammad SAW", "libur_nasional", "sedang", "Libur nasional resmi 2027 (SKB 3 Menteri)", "https://tanggalans.com/hari-libur-nasional-2027"),
]
w("data/kalender_momen.csv", H5, D5)

# ============ CHECKLIST ============
HC = ["dataset", "sumber", "status", "jumlah_baris", "tool_yang_dipakai", "alasan_jika_gagal"]
c = [
    ("1", "Google Trends - Trending now / Daily search trends (RSS geo=ID)", "berhasil", 10, "execute+fetch (RSS)"),
    ("1", "Google Trends - Interest over time 12 bulan", "berhasil", 10, "python pytrends"),
    ("1", "Google Trends - Interest over time 30 hari", "gagal", 0, "python pytrends + scraping endpoint widget", "Google kembalikan 400/429 (rate limit); dicoba pytrends 2x, payload lebih kecil, dan scraping langsung trends.google.com - tetap 429"),
    ("1", "Google Trends - Related queries (Rising & Top)", "berhasil", 55, "python pytrends"),
    ("1", "Google Trends - Related topics", "gagal", 0, "python pytrends", "IndexError parsing pytrends (endpoint berubah); dicoba 2x"),
    ("1", "Google Trends - Interest by region (provinsi)", "berhasil", 5, "python pytrends"),
    ("1", "Berita portal nasional (Google News RSS + Kompas/detik/CNBC/CNN/Kontan/Tirto)", "berhasil", 26, "execute+fetch RSS, tavily"),
    ("1", "TikTok - Trend Discovery / Creative Center", "sebagian", 10, "fetch API gagal (non-json); fallback agregator socialmediadefined.com + tavily extract"),
    ("1", "Instagram - hashtag & Reels trending", "sebagian", 2, "tavily + agregator iqhashtags/Dash Social", "Instagram tanpa API publik; data agregator global bukan khusus Indonesia"),
    ("1", "X/Twitter - trending Indonesia", "berhasil", 19, "fetch lagitren.id & getdaytrends.com (agregator publik)"),
    ("1", "YouTube - trending Indonesia", "sebagian", 5, "fetch + python requests + Playwright MCP + CreatorDB via tavily", "youtube.com/feed/trending redirect ke home dan menuntut login (dicoba 3 jalur); data diambil dari agregator CreatorDB/youtrendings"),
    ("1", "Reddit - thread ramai", "sebagian", 5, "tavily (API langsung diblokir)", "reddit.com & old.reddit JSON 403 untuk semua user-agent, termasuk python requests"),
    ("1", "Kaskus - thread ramai", "sebagian", 0, "fetch + tavily", "Halaman utama SPA/JS, thread tidak ada di HTML; diambil via tavily untuk dataset 2"),
    ("1", "Marketplace (Tokopedia/Shopee) - kata kunci naik", "sebagian", 3, "tavily (artikel analisis)", "Data kategori tren dari artikel, bukan API marketplace"),
    ("2", "Google - People also ask / Pencarian terkait", "sebagian", 0, "brightdata search_engine (Bing)", "PAA tidak diekspose di hasil SERP yang diterima"),
    ("2", "Google - autocomplete", "berhasil", 125, "execute+fetch suggest API (30 prefix)"),
    ("2", "Google Trends - related queries berbentuk pertanyaan", "berhasil", 21, "python pytrends"),
    ("2", "Reddit / forum", "sebagian", 5, "tavily", "API langsung 403; jalur alternatif pencarian"),
    ("2", "Kaskus", "sebagian", 2, "tavily", "Halaman utama SPA/JS; thread via pencarian"),
    ("2", "Quora", "gagal", 0, "execute+fetch + tavily", "Halaman topic dilayani tapi konten Q&A tidak terbaca tanpa login/JS; hasil pencarian tidak relevan"),
    ("2", "Komentar publik YouTube/TikTok/Instagram", "gagal", 0, "-", "Butuh API platform/akun; tidak tersedia di tool"),
    ("2", "Review pelanggan (Google Maps/Tokopedia/Shopee/Play Store)", "dilewati", 0, "-", "Mode umum tanpa industri; review tanpa konteks produk tidak relevan"),
    ("5", "Kalender libur resmi (SKB) via berita/agregator kalender", "berhasil", 11, "tavily"),
    ("5", "Hari besar nasional & internasional", "berhasil", 16, "tavily (Kompas TV, MetroTVNews, Suara)"),
    ("5", "Tanggal belanja e-commerce (11.11, 12.12, Harbolnas, Black Friday, gajian)", "berhasil", 8, "tavily"),
    ("5", "Event industri/pameran/konser", "berhasil", 9, "tavily (ICE BSD, exposale, jadwalevent, CNBC)"),
    ("5", "Momen viral dari dataset 1", "berhasil", 0, "terintegrasi ke catatan dataset 1", "Tidak ada momen viral yang bisa dipastikan turun ke kalender 60 hari"),
]
with open("data/_sumber_checklist.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(HC)
    wr.writerows(c)
print(f"data/_sumber_checklist.csv: {len(c)} baris")

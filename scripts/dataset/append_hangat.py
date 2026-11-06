# -*- coding: utf-8 -*-
"""Append isu-isu hangat terkini Indonesia ke tren_topik.csv dan pertanyaan_audiens.csv (tanpa duplikat)."""
import csv

TGL = "2026-11-06"

def append(path, header, rows, keycols):
    with open(path, encoding="utf-8-sig") as f:
        existing = list(csv.DictReader(f))
    seen = set("|".join(r[k].strip().lower() for k in keycols) for r in existing)
    added = 0
    for r in rows:
        key = "|".join(r[k].strip().lower() for k in keycols)
        if key in seen:
            continue
        seen.add(key)
        existing.append({**{h: "" for h in header}, **r})
        added += 1
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=header)
        wr.writeheader()
        wr.writerows(existing)
    print(f"{path}: +{added} baris -> total {len(existing)}")

H1 = ["tanggal_ambil", "kategori", "topik", "kata_kunci", "sumber", "indikator_tren", "skor_atau_volume", "sentimen", "source_url"]
URL_GN = "https://news.google.com/rss/search?hl=id&gl=ID&ceid=ID:id&q="
hangat = [
    ("lingkungan", "Karhutla Kalteng-Sumatera: BNPB kerahkan 51 ribu personel di 4 provinsi",
     "karhutla; kebakaran hutan; dry ice; water bombing",
     "Google News RSS (query: karhutla) + ANTARA/Kompas/RRI", "naik", "", "negatif",
     URL_GN + "karhutla"),
    ("lingkungan", "Helikopter TNI jatuh saat padamkan karhutla Seruyan: 1 gugur, 5 dievakuasi",
     "helikopter tni jatuh; karhutla kalteng",
     "Google News RSS (query: helikopter TNI jatuh)", "naik", "", "negatif",
     URL_GN + "helikopter+tni+jatuh"),
    ("lingkungan", "2 orangutan Fajar & Fitri dievakuasi dari karhutla Kalteng",
     "orangutan karhutla", "Google News RSS (query: karhutla)", "naik", "", "negatif", URL_GN + "karhutla"),
    ("hukum_keamanan", "Kasus penyadapan ilegal sasar Presiden: 3 perwita Polri ditahan, tersangka baru Slamet Uliandi",
     "penyadapan ilegal; reformasi polri",
     "Google News RSS (query: penyadapan ilegal) + ANTARA/20detik", "naik", "", "negatif",
     URL_GN + "penyadapan+ilegal"),
    ("hukum_energi", "Samin Tan: korupsi tata kelola tambang rugikan negara Rp17,7 T, cuci uang Rp18 T, sidang perdana pekan depan",
     "samin tan; tambang ilegal",
     "Google News RSS (query: samin tan tambang) + detik/Kompas", "naik", "", "negatif",
     URL_GN + "samin+tan+tambang"),
    ("politik", "Demo mahasiswa 28-29 Okt (Sumpah Pemuda): 53 aksi, Tritura disuarakan lagi, isu simbol tiga jari",
     "demo mahasiswa; sumpah pemuda; tritura; simbol tiga jari",
     "tavily (IDN Times, Kompas, BBC Indonesia)", "naik", "", "negatif",
     "https://www.idntimes.com/news/indonesia/13-fakta-demo-mahasiswa-28-29-oktober-2026-di-jakarta-00-7lwyz-g35dp2"),
    ("politik", "Kontroversi 'Sahabat Dahsyat': Polda Metro Jaya hapus unggahan foto bersama mahasiswa",
     "sahabat dahsyat; polda metro jaya",
     "tavily (utusan X @ferizandra, PANDUGA.ID)", "naik", "", "negatif",
     "https://x.com/Pandugaid/status/2116067478820520214"),
    ("politik_keamanan", "Isu pengerahan TNI saat demo: DPR menuntut kepatuhan prosedur hukum",
     "pengerahan tni demo", "tavily (gesuri.id)", "stabil", "", "netral",
     "https://www.gesuri.id/pemerintahan/pengerahan-tni-saat-demonstrasi-tb-hasanuddin-harus-sesuai-prosedur-hukum-b2qdcZbjcp"),
    ("kesehatan_sosial", "Program MBG: BGN aktifkan kembali 953 dapur, aturan pengurangan relawan SPPG diperjelas",
     "makan bergizi gratis; mbg; bgn",
     "Google News RSS (query: makan bergizi gratis) + CNN/Bloomberg Technoz", "naik", "", "netral",
     URL_GN + "makan+bergizi+gratis"),
    ("bansos", "BSU Rp900.000 November: jadwal pencairan untuk buruh/karyawan dan cara cek penerima online",
     "bsu; bansos november 2026",
     "Google News RSS (query: BSU bansos) + Kabar24/Bloomberg Technoz", "naik", "", "positif",
     URL_GN + "BSU+bansos"),
    ("kesehatan_sosial", "Isu ramai di Threads: PBI JKN desil 6-10 dinonaktifkan per 1 Nov - BPJS Kesehatan klarifikasi",
     "bpjs pbi desil 6-10; jkn nonaktif",
     "tavily (aksel.co.id, Liputan6)", "naik", "", "negatif",
     "https://kesehatan.liputan6.com/info-sehat/read/8325607/ramai-soal-peserta-pbi-desil-610-dinonaktifkan-per-1-november-ini-penjelasan-bpjs-kesehatan"),
    ("bansos", "Perlinsos Digital: 18 juta keluarga terdaftar, pendaftaran online PKH/BPNT ramai dicari",
     "perlinsos kemensos; daftar bansos online",
     "Google News RSS (query: perlinsos kemensos)", "naik", "", "netral",
     URL_GN + "perlinsos+kemensos"),
    ("ekonomi_ketenagakerjaan", "Isu PHK: Gudang Garam diterpa isu PHK massal (laba turun 87%), Disney PHK ribuan karyawan",
     "phk; gudang garam; phk massal",
     "tavily (IDN Times) + Google News RSS (query: PHK pekerja)", "naik", "", "negatif",
     "https://www.idntimes.com/business/economy/laba-drop-87-persen-gudang-garam-diterpa-isu-phk-massal-00-brqf5-2mxq6b"),
    ("finansial_global", "Bursa Asia kompak ambruk akibat koreksi saham AI: Kospi anjlok >8% dalam sehari",
     "kospi; saham ai; bursa asia",
     "Google News RSS (query: kospi saham asia) + CNBC", "naik", "", "negatif",
     URL_GN + "kospi+saham+asia"),
    ("finansial", "Binance kena peretasan (30 Okt): pelaku pasar waspadai volatilitas kripto",
     "binance hack; keamanan siber kripto",
     "tavily (Kontan)", "naik", "", "negatif",
     "https://investasi.kontan.co.id/news/pelaku-pasar-waspadai-volatilitas-harga-kripto-di-tengah-isu-keamanan-siber"),
    ("pangan", "Harga pangan naik menjelang Natal-Tahun Baru: beras Kalteng naik, cabai rawit & bawang terkerek",
     "harga beras; harga cabai rawit; pasokan pangan",
     "Google News RSS (query: harga beras pangan) + Databoks/InfoPublik", "naik", "", "negatif",
     URL_GN + "harga+beras+pangan"),
    ("infrastruktur", "Antisipasi banjir Jakarta: normalisasi 4 sungai dikebut hingga Desember, puncak hujan Feb 2027",
     "banjir jakarta; musim hujan 2026",
     "Google News RSS (query: banjir jakarta) + Kompas.id", "naik", "", "netral",
     URL_GN + "banjir+jakarta"),
    ("energi", "Shell resmi alihkan bisnis SPBU Indonesia ke SEFAS Group",
     "shell spbu; sefas group",
     "tavily (MetroTVNews)", "stabil", "", "netral",
     "https://www.metrotvnews.com/read/NQACRlZV-top-ekonomi-shell-resmi-alihkan-bisnis-spbu-indonesia-ke-sefas-group"),
    ("hiburan", "Raffi Ahmad & Willie Salim diboykot/hujat warganet dinilai pro-pemerintah",
     "raffi ahmad boikot",
     "tavily (lingkar.co)", "naik", "", "negatif",
     "https://lingkar.co/berita/kronologi-raffi-ahmad-kena-boikot-warganet-dan-dihujat-masyarakat"),
    ("olahraga_nasional", "Timnas Indonesia November 2026: 4 laga Garuda Muda, laga Yordania terancam batal",
     "timnas indonesia; jadwal timnas november",
     "tavily (aktualita.co)", "stabil", "", "netral",
     "https://aktualita.co/olahraga/jadwal-timnas-indonesia-november-2026-terbaru"),
    ("olahraga_nasional", "Persib menang historis di Melbourne; Super League: Persija (18 poin) diperebutkan Dewa United",
     "persib; persija; super league",
     "tavily (CNN Indonesia, Liputan6)", "naik", "", "positif",
     "https://www.cnnindonesia.com/olahraga/20261105171717-142-1423785/media-australia-kagum-aksi-suporter-persib-di-markas-melbourne-victory"),
]
append("data/tren_topik.csv", H1,
       [dict(zip(H1, (TGL, k, t, kw, s, i, sv, sen, u))) for k, t, kw, s, i, sv, sen, u in hangat],
       ["kategori", "topik"])

H2 = ["tanggal_ambil", "kategori", "pertanyaan_atau_keluhan", "sumber", "frekuensi_atau_jumlah_mention", "source_url"]
q2 = [
    ("bpjs_kesehatan", "Kenapa peserta BPJS PBI desil 6-10 dinonaktifkan per 1 November 2026? (isu ramai di Threads)",
     "Artikel berita aksel.co.id & Liputan6 (isu warganet)", "",
     "https://kesehatan.liputan6.com/info-sehat/read/8325607/ramai-soal-peserta-pbi-desil-610-dinonaktifkan-per-1-november-ini-penjelasan-bpjs-kesehatan"),
    ("bpjs_kesehatan", "Bagaimana cara cek status kepesertaan JKN dan mengaktifkan kembali PBI?",
     "Artikel berita aksel.co.id (isu warganet)", "",
     "https://aksel.co.id/bpjs-kesehatan-bantah-isu-nonaktif-pbi-desil-6-10-pada-1-november-2026"),
    ("kepegawaian", "Berapa besaran BSU Rp900.000 dan kapan jadwal pencairannya ke rekening buruh?",
     "Google News RSS (query: BSU bansos) - Kabar24", "",
     URL_GN + "BSU+bansos"),
    ("lingkungan", "Mengapa dry ice digunakan untuk mengatasi asap karhutla di Sumatera-Kalimantan?",
     "Kompas TV (artikel karhutla)", "",
     "https://www.kompas.tv/nasional/697708/mengapa-gunakan-dry-ice-atasi-asap-karhutla-di-sumatera-kalimantan"),
    ("lingkungan", "Kapan puncak musim hujan dan puncak rawan banjir Jakarta 2027?",
     "Kompas.id (artikel banjir Jakarta)", "",
     "https://kompas.id/baca/"),
    ("politik", "Mengapa gerakan protes di Indonesia dimotori Gen Z?",
     "BBC News Indonesia", "",
     "https://www.bbc.com/indonesia/articles/c620r2evrpd1o"),
    ("pangan", "Berapa harga beras, cabai rawit, dan bawang hari ini di daerah masing-masing?",
     "Databoks (harga pangan harian)", "",
     "https://databoks.katadata.co.id/"),
    ("kepegawaian", "Apakah korban PHK dihitung pengangguran? Penjelasan BPS soal korban PHK",
     "Kontan (artikel PHK/BPS)", "",
     "https://www.kontan.co.id/"),
]
append("data/pertanyaan_audiens.csv", H2,
       [dict(zip(H2, (TGL, k, q, s, f, u))) for k, q, s, f, u in q2],
       ["kategori", "pertanyaan_atau_keluhan"])

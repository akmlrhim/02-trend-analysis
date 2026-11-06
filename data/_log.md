# Log Pengumpulan Data Tren — 2026-11-06

Mode: industri agensi digital marketing / jasa digital, geo Indonesia, periode 30 hari terakhir.
Dataset 3 (konten_referensi) dan Dataset 4 (konten_akun_sendiri) **dilewati** karena `akun_referensi` dan `akun_sendiri` kosong.

## Pembersihan relevansi industri (iterasi ketiga, 6 Nov 2026)
Industri owner: **agensi digital marketing / jasa digital**. Data difilter ulang:
- Dibuang dari dataset 1: politik, hukum/kriminal (penyadapan, Samin Tan), lingkungan (karhutla), layanan publik, kesehatan, sains, bansos/BSU, finansial global (Kospi), infrastruktur, energi, demo mahasiswa, boikot selebriti.
- Ditambahkan 11 baris isu industri: Meta larang iklan TikTok di FB/IG (berlaku di Indonesia 8 Okt 2026, termasuk blokir deep-linking), Indonesia Digital MeetUp 2026 (27 juta UMKM), AI fatigue vs konten human-centric, UU PDP untuk pemasar, kreator keluhkan transparansi pendapatan (WCCE 2026), TikTok Awards Indonesia 2026, statistik 93 juta pengguna medsos, OJK pembiayaan UMKM digital, pergeseran media buying.
- Dibuang dari dataset 2: pertanyaan anatomi/kesehatan, sejarah, politik, migrasi, cuaca, denda otomotif, klaim BPJS/JHT, BPJS PBI.
- Ditambahkan 33 pertanyaan industri dari autocomplete: cara iklan (Meta/TikTok/IG/Threads/WhatsApp/Shopee/Google Ads), TikTok affiliate, cara promosi, naikkan followers, jualan online, jasa buat website, pajak/pinjaman/bantuan UMKM, QRIS, copywriting AI, digital marketing.


## Jumlah baris per file
| File | Baris |
|---|---|
| data/tren_topik.csv | 69 (target ≥40 ✓, 13 sumber termasuk Tempo.co & Campaign Indonesia) — murni relevansi industri: platform sosmed, e-commerce, iklan digital, UMKM klien |
| data/pertanyaan_audiens.csv | 65 (target ≥50 ✓, 4 sumber ✓) — murni relevansi industri: iklan platform, affiliate, jualan online, UMKM |
| data/kalender_momen.csv | 39 (mencakup 2026-11-07 s.d. 2027-01-05, 60 hari; semua momen kampanye relevan) |
| data/referensi_konten.csv | 23 (pemetaan isu terverifikasi menjadi sudut konten siap produksi, terhubung ke sumber) |
| data/_sumber_checklist.csv | 34 (satu baris per sumber + catatan pembersihan industri) |

## Otomatisasi mingguan (terpasang 6 Nov 2026)
- Tugas Windows Task Scheduler: **TrendRiset_RefreshMingguan**, berjalan tiap Senin 09.00.
- Pipeline: `scripts/refresh_weekly.py` (via `scripts/refresh_weekly.bat`, output log di `data/_refresh_log.txt`).
- Yang dilakukan: pytrends (trends/related/region) + berita industri 7 hari (Tempo, Campaign Indonesia via Google News RSS `site:` + `when:7d`) + trending X (dengan blokir kata politik dan filter tag sampah) + trending TikTok + autocomplete industri, semua di-append dengan dedupe lalu dinormalisasi.
- File `kalender_momen.csv`, `_sumber_checklist.csv`, dan `referensi_konten.csv` tidak diubah otomatis (butuh kurasi).
- Menjalankan manual kapan pun: `python scripts/refresh_weekly.py` dari root.

## Perubahan peruntukan
Sejak 6 Nov 2026, data riset ini dipakai sebagai **acuan pembuatan konten** untuk agensi. Pemetaan isu ke sudut konten, format saran, dan momen kalender tersedia di `data/referensi_konten.csv` dan halaman "Acuan Konten" di dashboard. Sudut konten adalah saran produksi; semua fakta yang dikutip tetap terhubung ke sumber di `source_url`.

## Isu hangat terkini yang tercakup (ditambahkan pada iterasi kedua)
Karhutla Kalteng-Sumatera (51 ribu personel BNPB, helikopter TNI jatuh, orangutan dievakuasi, dry ice), kasus penyadapan ilegal sasar Presiden, korupsi tambang Samin Tan, demo mahasiswa Sumpah Pemuda 28-29 Okt + kontroversi "Sahabat Dahsyat", isu BPJS PBI desil 6-10 (viral di Threads), BSU Rp900 ribu November, PHK massal Gudang Garam/Disney, crash saham AI/Kospi, hack Binance, harga pangan naik jelang Natal, banjir Jakarta, boikot Raffi Ahmad, Shell→SEFAS.

## MCP / tool yang tersedia dan dipakai
- **execute (Code Mode) + fetch** — RSS Google Trends trending-now, Google News RSS, Google autocomplete (suggest API), agregator lagitren.id & getdaytrends.com, socialmediadefined.com, uji endpoint TikTok Creative Center, Reddit, Kaskus, Quora, YouTube.
- **python 3.12 + pytrends (pip install)** — interest over time 12 bulan, related queries (Rising/Top), interest by region (provinsi). Raw JSON disimpan di `data/_pytrends_raw.json`.
- **MCP tavily** — tavily_search (kalender libur SKB, hari besar, Harbolnas, event, tren TikTok/X/YouTube/Instagram, marketplace, thread Reddit/Kaskus) dan tavily_extract (CreatorDB, TikTok trending). Catatan: parameter `country` membuat hasil kosong; dipakai tanpa parameter itu.
- **MCP brightdata** — search_engine Bing untuk uji "People also ask"/pencarian terkait (PAA tidak diekspose pada hasil).
- **MCP playwright** — render youtube.com/feed/trending; hasil redirect ke home + tuntut login → ditutup, tidak dipakai lebih lanjut.
- **websearch bawaan** — gagal total (HTTP 402, tanpa kuota) → diganti tavily/brightdata/fetch.
- MCP apify & firecrawl tersedia tetapi tidak diperlukan setelah sumber di atas berhasil.

## Urutan fallback sesuai aturan (MCP dulu → scraping Python)
1. Reddit: fetch JSON (403) → old.reddit JSON/HTML (403) → api.reddit.com (403) → python requests old.reddit (403) → **tavily site:reddit.com** ✓ (5 baris D2).
2. YouTube trending: fetch (shell page) → consent cookie (kosong) → python requests ytInitialData (kosong) → **Playwright MCP** (redirect ke home, butuh login) → **agregator CreatorDB/youtrendings via tavily** ✓ (5 baris).
3. TikTok Creative Center: API endpoint non-JSON → **agregator socialmediadefined.com via tavily_extract** ✓ (10 baris).
4. Trends interest over time 30 hari: pytrends (400) → payload kecil (400) → today 1-m / now 7-d (429) → python scraping endpoint widget (429). **Gagal permanen (rate limit)** — hanya 12 bulan yang tersedia.
5. Kaskus: homepage fetch (SPA/JS, tidak ada thread di HTML) → /hot (404) → **tavily site:kaskus.co.id** ✓ (2 baris D2).
6. Google News: RSS resmi ✓ langsung.

## Kendala
- Google Trends rate-limit (429/400) untuk timeframe 30 hari/1 bulan/7 hari dan related topics — hanya 12 bulan berhasil.
- Reddit & Quora diblokir tanpa login; komentar publik YouTube/TikTok/Instagram butuh API/akun — ditandai "perlu akses akun" di checklist.
- Instagram: tidak ada data tren khusus Indonesia dari sumber publik; hanya agregator hashtag global (ditandai sebagian).
- Review pelanggan (Google Maps/Tokopedia/Shopee) dilewati: mode umum tanpa industri, review tanpa konteks produk tidak relevan.
- Berita Google News menggunakan URL redirect news.google.com (valid, tapi panjang).

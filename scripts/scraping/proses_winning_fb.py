# -*- coding: utf-8 -*-
"""
Proses data mentah konten Facebook Impost Media (@propeaagency) menjadi
dataset siap analisa & klasifikasi winning/normal/losing.

Sumber: file JSON output Apify `apify/facebook-posts-scraper`
(data/konten_winning/_raw/fb_propeaagency, 236 post Mar 2025-Okt 2026).
Output: data/konten_winning/facebook_propeaagency.csv + baris ringkasan_akun.csv.

Catatan metrik: FB menyembunyikan jumlah like/komentar/share di sebagian besar
post (nilainya 0/kosong, sama seperti IG), tapi viewsCount tersedia untuk
video. Klasifikasi winning memakai views; post tanpa views -> tanpa_data.
Jalankan dari root: python scripts/scraping/proses_winning_fb.py
"""
import json
import os
import re
import pandas as pd

TOOL_OUT = os.path.join("data", "konten_winning", "_raw")
OUT_DIR = "data/konten_winning"
F_FB = "fb_propeaagency"  # FB @propeaagency (halaman FB Impost Media)

load = lambda f: json.load(open(os.path.join(TOOL_OUT, f), encoding="utf-8"))

# ------------------------------------------------ facebook @propeaagency
fb_raw = load(F_FB)
df_fb = pd.DataFrame([{
    "id": x.get("postId"),
    "platform": "facebook",
    "akun": "propeaagency",
    "url": x.get("url"),
    "teks": x.get("text"),
    "tanggal": x.get("time"),
    # FB menyembunyikan like/share bila 0 -> simpan None, bukan 0 palsu
    "likes": x.get("likes") if x.get("likes") else None,
    "komentar": x.get("comments") if x.get("comments") else None,
    "share": x.get("shares") if x.get("shares") else None,
    "views": x.get("viewsCount") or x.get("videoPostViewCount"),
    "format": ("reels" if "/reel/" in str(x.get("url") or "")
               else "video" if x.get("isVideo")
               else "foto" if (x.get("media") or {}).get("__typename") == "Photo"
               else "lainnya"),
    "hashtags": ", ".join(sorted(set(re.findall(r"#([\w\u00C0-\u024F]+)", str(x.get("text") or ""))))),
} for x in fb_raw]).drop_duplicates(subset="id")

# ------------------------------------------------ fitur waktu & topik (aturan sama dgn proses_winning.py)
HARI = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}

def tanggal_fix(s):
    return pd.to_datetime(s, errors="coerce", utc=True).dt.tz_convert("Asia/Jakarta")

TOPIC_RULES = [
    ("rekrutmen", r"(lowongan|loker|magang|hiring|kirim cv|hrd|PKL|karier|portofolio terbaikmu|we are hiring)"),
    ("hari_besar", r"(selamat hari|dirgahayu|idul|lebaran|muharram|kartini|merdeka|hut ri|sumpah pemuda|pancasila|kenaikan|natal|hari buruh|pendidikan nasional|hut ke)"),
    ("jualan_klien", r"(konsultasi|klien kami|roas|omzet|slot bulan ini|garansi|dm \"|dm kami|klik link di bio|jasa impost|pakai jasa|impost media bantu)"),
    ("portfolio_showcase", r"(hasil kerja|kumpulan desain|best reels|best creations|project|beberapa hasil|cuplikan|karya|bekerja sama dengan|bersama [A-Z])"),
    ("edukasi", r"(tips|cara|kenapa|metrik|strategi|algoritma|insight|save|carousel|hook|branding|content|conten|views|reach|posting|konten(kamu|mu)? bisa|jangan)"),
]

def klas_topik(t):
    t = str(t or "").lower()
    for nama, pat in TOPIC_RULES:
        if re.search(pat, t, re.IGNORECASE):
            return nama
    return "lainnya"

t = tanggal_fix(df_fb["tanggal"])
df_fb["tanggal_jakarta"] = t.dt.strftime("%Y-%m-%d %H:%M")
df_fb["hari"] = t.dt.day_of_week.map(HARI)
df_fb["jam"] = t.dt.hour
df_fb["topik"] = df_fb["teks"].apply(klas_topik)
df_fb["panjang_teks"] = df_fb["teks"].astype(str).str.len()

# ------------------------------------------------ engagement & klasifikasi winning
df_fb["views"] = pd.to_numeric(df_fb["views"], errors="coerce")
df_fb["engagement"] = df_fb[["likes", "komentar", "share"]].fillna(0).sum(axis=1)
df_fb["er_views"] = (df_fb["engagement"] / df_fb["views"].mask(df_fb["views"] == 0) * 100).round(2)

def klasifikasi(df, metrik):
    p75 = df[metrik].quantile(0.75)
    p25 = df[metrik].quantile(0.25)
    def k(v):
        if pd.isna(v):
            return "tanpa_data"
        if v >= p75:
            return "WINNING"
        if v <= p25:
            return "losing"
        return "normal"
    return df[metrik].apply(k)

df_fb["status"] = klasifikasi(df_fb, "views")

# ------------------------------------------------ simpan
df_fb.sort_values("tanggal_jakarta", ascending=False).to_csv(f"{OUT_DIR}/facebook_propeaagency.csv", index=False)

# perbarui baris ringkasan akun (buat ulang baris FB, baris lain tak disentuh)
ringkas_path = f"{OUT_DIR}/ringkasan_akun.csv"
ringkas = pd.read_csv(ringkas_path)
ringkas = ringkas[ringkas["akun"] != "@propeaagency (facebook)"]
baris_fb = pd.DataFrame([{
    "platform": "facebook", "akun": "@propeaagency (facebook)", "followers": pd.NA,
    "post": len(df_fb),
    "winning": int((df_fb["status"] == "WINNING").sum()),
    "med_views": df_fb["views"].median(),
    "er_median": df_fb["er_views"].median(),
}])
ringkas = pd.concat([ringkas, baris_fb], ignore_index=True)
ringkas.to_csv(ringkas_path, index=False)

# ------------------------------------------------ ringkasan cepat
pd.set_option("display.width", 200)
print("=== FB @propeaagency:", len(df_fb), "post, rentang",
      df_fb["tanggal"].min(), "->", df_fb["tanggal"].max())
print(df_fb.groupby("status")["views"].agg(["count", "median"]).round(0))
print("\nFormat FB:")
print(df_fb.groupby("format").agg(n=("views", "size"), med_views=("views", "median"),
                                  med_likes=("likes", "median"), med_share=("share", "median")).round(1))
print("\nTopik FB (median views | n):")
print(df_fb.groupby("topik").agg(n=("views", "size"), med_views=("views", "median"),
                                 med_eng=("engagement", "median")).round(0).sort_values("med_views", ascending=False))
print("\nHari posting FB (median views):")
print(df_fb.groupby("hari").agg(n=("views", "size"), med_views=("views", "median")).round(0))
print("\nTop 10 FB views:")
print(df_fb.nlargest(10, "views")[["format", "topik", "views", "likes", "share", "tanggal_jakarta"]].to_string(index=False))

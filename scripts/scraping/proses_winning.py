# -*- coding: utf-8 -*-
"""
Proses data mentah konten Impost Media (IG + TikTok) + benchmark
menjadi dataset siap analisa & klasifikasi winning/normal/losing.

Sumber: output tool (JSON) dari Apify MCP, file di ~/.local/share/opencode/tool-output/.
Output: data/konten_winning/*.csv
"""
import json
import os
import re
import pandas as pd

TOOL_OUT = os.path.join("data", "konten_winning", "_raw")
OUT_DIR = "data/konten_winning"
os.makedirs(OUT_DIR, exist_ok=True)

F_TT = "tool_1c408c9260016mqBayir4FK9Kv"      # TikTok @impostmedia (part1+part2)
F_IG = "tool_1c408eed3001cbrbeWNSveGxHe"      # IG @impostmedia (caption) + IG benchmark
F_IMPEEPS = "ig_impeeps"                      # IG @impeeps.ofc (akun Gen Z Impost, 184 post)
F_BENCH = "tool_1c409a527001buifXApSxp8fmV"   # TikTok benchmark + FB searches (tidak dipakai: fokus Impost saja)

load = lambda f: json.load(open(os.path.join(TOOL_OUT, f), encoding="utf-8"))

# ------------------------------------------------ tiktok sendiri
tt = load(F_TT)
tt_items = [x for x in (tt["part1"] + tt["part2"]) if x.get("id")]
df_tt = pd.DataFrame([{
    "id": x.get("id"),
    "platform": "tiktok",
    "akun": "impostmedia",
    "url": x.get("webVideoUrl"),
    "teks": x.get("text"),
    "tanggal": x.get("createTimeISO"),
    "views": x.get("playCount"),
    "likes": x.get("diggCount"),
    "komentar": x.get("commentCount"),
    "share": x.get("shareCount"),
    "simpan": x.get("collectCount"),
    "format": "slideshow" if x.get("isSlideshow") else "video",
    "durasi_detik": x.get("videoMeta.duration"),
    "pinned": x.get("isPinned"),
    "iklan": x.get("isSponsored"),
    "hashtags": ", ".join(x.get("hashtags.name") or x.get("hashtags") or []),
} for x in tt_items]).drop_duplicates(subset="id")

# ------------------------------------------------ tiktok benchmark
bench = load(F_BENCH)
df_ttb = pd.DataFrame([{
    "id": x.get("id"),
    "platform": "tiktok",
    "akun": "benchmark_" + str(x.get("authorMeta.name")),
    "url": x.get("webVideoUrl"),
    "teks": x.get("text"),
    "tanggal": x.get("createTimeISO"),
    "views": x.get("playCount"),
    "likes": x.get("diggCount"),
    "komentar": x.get("commentCount"),
    "share": x.get("shareCount"),
    "simpan": x.get("collectCount"),
    "format": "slideshow" if x.get("isSlideshow") else "video",
    "durasi_detik": x.get("videoMeta.duration"),
    "pinned": x.get("isPinned"),
    "iklan": x.get("isSponsored"),
    "followers_akun": x.get("authorMeta.fans"),
    "hashtags": ", ".join(x.get("hashtags.name") or x.get("hashtags") or []),
} for x in bench.get("ttBench", [])]).drop_duplicates(subset="id")

# ------------------------------------------------ instagram
def ig_rows(items, label):
    rows = []
    for x in items:
        likes = x.get("likesCount")
        rows.append({
            "shortCode": x.get("shortCode"),
            "platform": "instagram",
            "akun": label,
            "owner_username": x.get("ownerUsername"),
            "url": x.get("url"),
            "teks": x.get("caption"),
            "tanggal": x.get("timestamp"),
            "likes": likes if likes and likes >= 0 else None,
            "komentar": x.get("commentsCount"),
            "views": x.get("videoViewCount"),
            "format": {"Video": "reels", "Sidecar": "carousel", "Image": "foto"}.get(x.get("type"), x.get("type")),
            "co_author": x.get("ownerUsername") not in (label, "impostmedia"),
            "hashtags": ", ".join(x.get("hashtags") or []),
        })
    return rows

ig_raw = load(F_IG)
df_ig = pd.DataFrame(ig_rows(ig_raw["igOwn"], "impostmedia")).drop_duplicates(subset="shortCode")
df_igb = pd.DataFrame(ig_rows(ig_raw["igBench"], "impostmedia")).drop_duplicates(subset="shortCode")
# akun benchmark berbeda-beda: pakai owner_username sebagai nama akun
df_igb["akun"] = "benchmark_" + df_igb["owner_username"].astype(str)

# ------------------------------------------------ IG @impeeps.ofc (akun kedua Impost, 553 followers)
igp_raw = load(F_IMPEEPS)
df_igp = pd.DataFrame(ig_rows(igp_raw.get("items", igp_raw.get("igOwn", [])), "impeeps.ofc")).drop_duplicates(subset="shortCode")
# post milik @impostmedia yang ikut ke-feed impeeps (kolaborasi) sudah ada di df_ig → buang duplikat
df_igp = df_igp[df_igp["owner_username"] == "impeeps.ofc"].copy()
df_igp["co_author"] = False
# scrape awal impeeps tidak menyimpan caption/hashtags -> gabungkan dari scrape ulang
# (raw ig_impeeps_v2, Feb-Okt 2026) berdasarkan shortCode; post lama tanpa caption tetap kosong
igp_v2 = load("ig_impeeps_v2")
df_igp_v2 = pd.DataFrame([{
    "shortCode": x.get("shortCode"),
    "teks_v2": x.get("caption"),
    "hashtags_v2": ", ".join(x.get("hashtags") or []),
} for x in igp_v2]).drop_duplicates(subset="shortCode")
df_igp = df_igp.merge(df_igp_v2, on="shortCode", how="left")
kosong_teks = df_igp["teks"].isna() | (df_igp["teks"].astype(str).str.strip() == "")
df_igp.loc[kosong_teks, "teks"] = df_igp.loc[kosong_teks, "teks_v2"]
kosong_h = df_igp["hashtags"].isna() | (df_igp["hashtags"].astype(str).str.strip() == "")
df_igp.loc[kosong_h, "hashtags"] = df_igp.loc[kosong_h, "hashtags_v2"]
df_igp = df_igp.drop(columns=["teks_v2", "hashtags_v2"])
FOLLOWERS_IMPEEPS = 553

# ------------------------------------------------ fitur waktu & topik
HARI = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}

def tanggal_fix(s):
    return pd.to_datetime(s, errors="coerce", utc=True).dt.tz_convert("Asia/Jakarta")

TOPIC_RULES = [
    ("rekrutmen", r"(lowongan|loker|magang|hiring|kirim cv|hrd|PKL|karier|portofolio terbaikmu)"),
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

for df in (df_tt, df_ttb, df_ig, df_igb, df_igp):
    t = tanggal_fix(df["tanggal"])
    df["tanggal_jakarta"] = t.dt.strftime("%Y-%m-%d %H:%M")
    df["hari"] = t.dt.weekday.map(HARI)
    df["jam"] = t.dt.hour
    df["topik"] = df["teks"].apply(klas_topik)
    df["panjang_teks"] = df["teks"].astype(str).str.len()

# ------------------------------------------------ engagement
df_tt["engagement"] = df_tt[["likes", "komentar", "share", "simpan"]].fillna(0).sum(axis=1)
df_tt["er_views"] = (df_tt["engagement"] / df_tt["views"].replace(0, pd.NA) * 100).astype(float).round(2)

df_ttb["engagement"] = df_ttb[["likes", "komentar", "share", "simpan"]].fillna(0).sum(axis=1)
df_ttb["er_views"] = (df_ttb["engagement"] / df_ttb["views"].replace(0, pd.NA) * 100).astype(float).round(2)

FOLLOWERS_IG = 17588
for df, fol in ((df_ig, FOLLOWERS_IG), (df_igb, FOLLOWERS_IG), (df_igp, FOLLOWERS_IMPEEPS)):
    df["engagement"] = df[["likes", "komentar"]].fillna(0).sum(axis=1)
    df["er_followers"] = (df["engagement"] / fol * 100).round(3)

# segmen IG akun impostmedia: konten akun utama vs kolaborasi co-author @impeeps.ofc
df_ig["segmen"] = df_ig["co_author"].map({False: "akun_utama", True: "kolab_impeeps"})

# ------------------------------------------------ klasifikasi winning
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

df_tt["status"] = klasifikasi(df_tt, "views")          # distribusi views
df_ttb["status"] = klasifikasi(df_ttb, "views")
# IG: klasifikasi per segmen/akun (akun utama vs kolaborasi vs impeeps.ofc) karena skalanya beda jauh
df_ig["status"] = (
    df_ig.groupby("segmen", group_keys=False)
    .apply(lambda g: klasifikasi(g, "engagement"), include_groups=False)
)
df_igp["status"] = klasifikasi(df_igp, "engagement")
df_igb["status"] = klasifikasi(df_igb, "engagement")

# ------------------------------------------------ simpan
df_tt.sort_values("tanggal_jakarta", ascending=False).to_csv(f"{OUT_DIR}/tiktok_impostmedia.csv", index=False)
# df_ttb.sort_values("views", ascending=False).to_csv(f"{OUT_DIR}/tiktok_benchmark.csv", index=False)
df_ig.sort_values("tanggal_jakarta", ascending=False).to_csv(f"{OUT_DIR}/instagram_impostmedia.csv", index=False)
# df_igb.sort_values("views" if "views" in df_igb else "engagement", ascending=False).to_csv(f"{OUT_DIR}/instagram_benchmark.csv", index=False)
df_igp.sort_values("tanggal_jakarta", ascending=False).to_csv(f"{OUT_DIR}/instagram_impeeps.csv", index=False)

# ringkasan per akun utk dashboard
ringkas = pd.concat([
    pd.DataFrame([{"platform": "tiktok", "akun": "@impostmedia", "followers": 177, "post": len(df_tt),
                   "winning": int((df_tt["status"] == "WINNING").sum()),
                   "med_views": df_tt["views"].median(), "er_median": df_tt["er_views"].median()}]),
    pd.DataFrame([{"platform": "instagram", "akun": "@impostmedia (utama)", "followers": FOLLOWERS_IG,
                   "post": int((df_ig["segmen"] == "akun_utama").sum()),
                   "winning": int(((df_ig["segmen"] == "akun_utama") & (df_ig["status"] == "WINNING")).sum()),
                   "med_views": pd.NA,
                   "er_median": df_ig.loc[df_ig["segmen"] == "akun_utama", "er_followers"].median()}]),
    pd.DataFrame([{"platform": "instagram", "akun": "@impostmedia (kolab impeeps)", "followers": FOLLOWERS_IG,
                   "post": int((df_ig["segmen"] == "kolab_impeeps").sum()),
                   "winning": int(((df_ig["segmen"] == "kolab_impeeps") & (df_ig["status"] == "WINNING")).sum()),
                   "med_views": pd.NA,
                   "er_median": df_ig.loc[df_ig["segmen"] == "kolab_impeeps", "er_followers"].median()}]),
    pd.DataFrame([{"platform": "instagram", "akun": "@impeeps.ofc", "followers": FOLLOWERS_IMPEEPS, "post": len(df_igp),
                   "winning": int((df_igp["status"] == "WINNING").sum()),
                   "med_views": pd.NA,
                   "er_median": df_igp["er_followers"].median()}]),
])
# pertahankan baris Facebook (dikelola proses_winning_fb.py) agar tidak hilang saat skrip ini dijalankan ulang
fb_ringkas_path = f"{OUT_DIR}/facebook_propeaagency.csv"
if os.path.exists(fb_ringkas_path):
    ringkas_lama = pd.read_csv(f"{OUT_DIR}/ringkasan_akun.csv")
    baris_fb_lama = ringkas_lama[ringkas_lama["akun"] == "@propeaagency (facebook)"]
    if not baris_fb_lama.empty:
        ringkas = pd.concat([ringkas, baris_fb_lama], ignore_index=True)
ringkas.to_csv(f"{OUT_DIR}/ringkasan_akun.csv", index=False)

# ------------------------------------------------ ringkasan cepat
pd.set_option("display.width", 200)
print("=== TIKTOK @impostmedia:", len(df_tt), "post, rentang", df_tt["tanggal"].min(), "->", df_tt["tanggal"].max())
print(df_tt.groupby("status")["views"].agg(["count", "median"]).round(0))
print("\nTopik TikTok (median views | n):")
print(df_tt.groupby("topik").agg(n=("views", "size"), med_views=("views", "median"), med_likes=("likes", "median")).round(0).sort_values("med_views", ascending=False))
print("\nFormat TikTok:")
print(df_tt.groupby("format").agg(n=("views", "size"), med_views=("views", "median"), med_er=("er_views", "median")).round(1))
print("\nHari posting TikTok (median views):")
print(df_tt.groupby("hari").agg(n=("views", "size"), med_views=("views", "median")).round(0))
print("\n=== IG @impostmedia:", len(df_ig), "post")
print("likes tersedia:", df_ig["likes"].notna().sum(), "| status:")
print(df_ig.groupby("status")["engagement"].agg(["count", "median"]))
print("\nTopik IG:")
print(df_ig.groupby("topik").agg(n=("engagement", "size"), med_eng=("engagement", "median"), med_komentar=("komentar", "median")).round(1).sort_values("med_eng", ascending=False))
print("\nFormat IG:")
print(df_ig.groupby("format").agg(n=("engagement", "size"), med_eng=("engagement", "median"), med_komentar=("komentar", "median")).round(1))
print("\nTop 10 IG engagement:")
print(df_ig.nlargest(10, "engagement")[["format", "topik", "likes", "komentar", "owner_username", "tanggal_jakarta"]].to_string(index=False))
print("\n=== IG benchmark:", len(df_igb), "post dari", df_igb["owner_username"].nunique(), "akun")
print(df_igb.groupby("owner_username").agg(n=("engagement", "size"), med_eng=("engagement", "median"), med_komentar=("komentar", "median")).round(1))
print("\n=== TikTok benchmark:", len(df_ttb), "video")
print(df_ttb[["views", "engagement", "er_views"]].describe().round(1))

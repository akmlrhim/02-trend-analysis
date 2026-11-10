# -*- coding: utf-8 -*-
"""Analisa mendalam khusus konten Impost Media (TikTok + IG)."""
import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd, re

d = "data/konten_winning"
pd.set_option("display.width", 220)
tt = pd.read_csv(f"{d}/tiktok_impostmedia.csv")
ig = pd.read_csv(f"{d}/instagram_impostmedia.csv")

# --- fitur konten TikTok
tt["ada_cta"] = tt["teks"].str.contains(r"(konsult|DM |dm |klik link|slot bulan|gratiss?|follow akun|save|simpan|komen|koment|tag |share ke)", case=False, na=False)
tt["ada_hook_pertanyaan"] = tt["teks"].str.match(r"^\s*(Pernah|Kenapa|Gimana|Udah|Kadang|Masih|Mau|Sering|Boleh|Siapa|Apa)", na=False)
tt["n_hashtag"] = tt["hashtags"].fillna("").str.split(",").apply(lambda x: len([h for h in x if h.strip()]))
tt["impost_tag"] = tt["hashtags"].fillna("").str.lower().str.contains("impostmedia")
tt["panjang"] = tt["teks"].astype(str).str.len()
win = tt["status"] == "WINNING"

print("== CTA vs views ==")
print(tt.groupby("ada_cta").agg(n=("views","size"), med=("views","median"), med_er=("er_views","median")).round(1))
print("\n== Hook pertanyaan vs views ==")
print(tt.groupby("ada_hook_pertanyaan").agg(n=("views","size"), med=("views","median"), med_er=("er_views","median")).round(1))
print("\n== Jumlah hashtag ==")
tt["htag_bin"] = pd.cut(tt["n_hashtag"], [-1,1,3,5,50], labels=["0-1","2-3","4-5",">5"])
print(tt.groupby("htag_bin", observed=True).agg(n=("views","size"), med=("views","median")).round(0))
print("\n== Tag impostmedia di hashtag ==")
print(tt.groupby("impost_tag").agg(n=("views","size"), med=("views","median")).round(0))
print("\n== Panjang teks ==")
tt["panjang_bin"] = pd.cut(tt["panjang"], [0,150,400,800,99999], labels=["<150","150-400","400-800",">800"])
print(tt.groupby("panjang_bin", observed=True).agg(n=("views","size"), med=("views","median")).round(0))
print("\n== Winning (>=693 views) karakteristik ==")
print(tt[win].groupby("format").size(), "| CTA:", int(tt[win]["ada_cta"].sum()), "/", int(win.sum()), "| slideshow:", int((tt[win]["format"]=="slideshow").sum()))
print("Rentang tanggal winning:", tt[win]["tanggal_jakarta"].str[:10].min(), "->", tt[win]["tanggal_jakarta"].str[:10].max())
print("Median ER winning:", round(tt[win]["er_views"].median(),2), "| median simpan winning:", tt[win]["simpan"].median())

# --- 25 winning teratas utk identifikasi pola manual
print("\n== 25 posting winning TikTok (urut views) ==")
for _, r in tt.nlargest(25, "views").iterrows():
    teks = str(r["teks"]).replace("\n", " ")[:75]
    print(f"{r['tanggal_jakarta'][:10]} {int(r['views']):>6}v ER{r['er_views']:>6}% {r['format']:<9} {str(r['topik'])[:16]:<16} {teks}")

# --- IG akun utama: komentar >0 (satu-satunya sinyal konsisten)
print("\n== IG akun utama: post dgn komentar > 0 ==")
utama = ig[ig["co_author"] == False]
k = utama[utama["komentar"] > 0]
print(len(k), "post dari", len(utama), "| median komentar:", k["komentar"].median())
print(k[["format","topik","likes","komentar","tanggal_jakarta"]].sort_values("komentar", ascending=False).head(12).to_string(index=False))

# --- IG kolaborasi impeeps: pola
print("\n== IG kolaborasi @impeeps.ofc (19 reels) ==")
kollab = ig[ig["co_author"] == True]
print(kollab[["likes","komentar","tanggal_jakarta"]].sort_values("likes", ascending=False).to_string(index=False))
print("median likes:", kollab["likes"].median(), "| median komentar:", kollab["komentar"].median())

# --- konsistensi: kesenjangan posting TikTok 2026
tt["bulan"] = pd.to_datetime(tt["tanggal"]).dt.strftime("%Y-%m")
print("\n== Frekuensi posting TikTok 2026 vs performa ==")
agg = tt.groupby("bulan").agg(n=("views","size"), med=("views","median"))
print(agg.tail(12).round(0))

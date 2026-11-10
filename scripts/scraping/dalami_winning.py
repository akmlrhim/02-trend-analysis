# -*- coding: utf-8 -*-
import pandas as pd, json, os
import sys; sys.stdout.reconfigure(encoding="utf-8")
d = "data/konten_winning"
pd.set_option("display.width", 220)

tt = pd.read_csv(f"{d}/tiktok_impostmedia.csv")
tt["bulan"] = pd.to_datetime(tt["tanggal"]).dt.strftime("%Y-%m")

print("== Tren bulanan TikTok (median views | jumlah post) ==")
print(tt.groupby("bulan").agg(n=("views","size"), med=("views","median"), med_likes=("likes","median")).round(0).tail(14))

print("\n== Topik x Format (median views) ==")
print(tt.pivot_table(index="topik", columns="format", values="views", aggfunc="median").round(0))

print("\n== Durasi vs views (video saja) ==")
v = tt[tt["format"]=="video"].copy()
v["dur_bin"] = pd.cut(v["durasi_detik"], [0,15,30,60,90,150,9999], labels=["<15s","15-30s","30-60s","60-90s","90-150s",">150s"])
print(v.groupby("dur_bin", observed=True).agg(n=("views","size"), med=("views","median")).round(0))

print("\n== TOP 15 winning TikTok ==")
top = tt.nlargest(15, "views")[["tanggal_jakarta","views","likes","komentar","share","simpan","er_views","format","topik","teks"]]
for _, r in top.iterrows():
    teks = str(r["teks"]).replace("\n"," ")[:70]
    print(f"{r['tanggal_jakarta'][:10]} | {int(r['views']):>6} views | ER {r['er_views']:>5}% | {r['format']:<9} | {r['topik']:<16} | {teks}")

print("\n== ER (engagement/views) bulanan terakhir ==")
print(tt.groupby("bulan")["er_views"].median().round(1).tail(12))

print("\n== IG: kolaborasi impeeps.ofc vs konten akun utama ==")
ig = pd.read_csv(f"{d}/instagram_impostmedia.csv")
print(ig.groupby("co_author").agg(n=("engagement","size"), med_eng=("engagement","median"), max_eng=("engagement","max"), med_komentar=("komentar","median")).round(1))

print("\n== IG benchmark: medians (banding akun) ==")
igb = pd.read_csv(f"{d}/instagram_benchmark.csv")
print(igb.groupby("owner_username").agg(n=("engagement","size"), med_likes=("likes","median"), med_eng=("engagement","median")).round(1))

print("\n== IG: topik x format ==")
print(ig.pivot_table(index="topik", columns="format", values="komentar", aggfunc="median").round(1))

print("\n== TikTok benchmark: top 10 ==")
ttb = pd.read_csv(f"{d}/tiktok_benchmark.csv")
for _, r in ttb.nlargest(10, "views").iterrows():
    print(f"{str(r['akun']):<28} {int(r['views']):>7} views ER {r['er_views']}% | {str(r['teks'])[:60].replace(chr(10),' ')}")

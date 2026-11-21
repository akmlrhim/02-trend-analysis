# -*- coding: utf-8 -*-
"""Tambahkan post terbaru hasil scraping browser MCP ke dataset konten winning.

Sumber: data/konten_winning/_raw/terbaru_2026-11-21.json (atau argumen path pertama).
Aman dijalankan ulang: dedupe memakai shortCode / id.
Metrik yang tidak tersedia untuk pengunjung tanpa login sengaja dikosongkan
(engagement kosong, status 'tanpa_data') agar tidak mengubah distribusi WINNING.
"""
import csv
import json
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/konten_winning/_raw/terbaru_2026-11-21.json"
OUT = "data/konten_winning"
HARI = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}

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


def baca(nama):
    with open(f"{OUT}/{nama}.csv", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def tulis(nama, header, rows):
    with open(f"{OUT}/{nama}.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def tanggalinfo(s):
    d = datetime.strptime(s[:10], "%Y-%m-%d")
    return d.strftime("%Y-%m-%d"), HARI[d.weekday()], (d.hour if " " in s else "")


def basis(teks, tanggal):
    tgl, hari, jam = tanggalinfo(tanggal)
    jakarta = tanggal.replace("T", " ")[:16] if " " in tanggal else tgl
    return dict(tanggal=tgl, tanggal_jakarta=jakarta, hari=hari, jam=jam,
                topik=klas_topik(teks), panjang_teks=len(teks),
                hashtags=", ".join(re.findall(r"#\w+", teks)), status="tanpa_data")


raw = json.load(open(RAW, encoding="utf-8"))
ringkasan = "ringkasan_akun.csv"
header_ring, rows_ring = baca("ringkasan_akun")
tambahan = {"@impostmedia (utama)": 0, "@impeeps.ofc": 0, "@propeaagency (facebook)": 0}

# ------------------------------------------------ Instagram
for file, akun_label, segmen in (
    ("instagram_impostmedia", "@impostmedia (utama)", "akun_utama"),
    ("instagram_impeeps", "@impeeps.ofc", None),
):
    header, rows = baca(file)
    ada = {r["shortCode"] for r in rows}
    n = 0
    for x in raw["instagram"]:
        if x["akun"] not in ("impostmedia", "impeeps.ofc") or x["code"] in ada:
            continue
        label = "@impostmedia (utama)" if x["akun"] == "impostmedia" else "@impeeps.ofc"
        if label == "@impostmedia (utama)" and file != "instagram_impostmedia":
            continue
        if label == "@impeeps.ofc" and file != "instagram_impeeps":
            continue
        baris = {
            "shortCode": x["code"], "platform": "instagram", "akun": x["akun"],
            "owner_username": x["akun"], "url": x["url"], "teks": x["teks"],
            "likes": "", "komentar": x.get("komentar", ""), "views": "",
            "format": x.get("format", "foto"), "co_author": False,
        }
        baris.update(basis(x["teks"], x["tanggal"]))
        baris["engagement"] = ""  # like tidak tersedia untuk tamu
        baris["er_followers"] = ""
        if segmen:
            baris["segmen"] = segmen
        rows.append({**{h: "" for h in header}, **baris})
        tambahan[label] += 1
        ada.add(x["code"])
        n += 1
    tulis(file, header, rows)
    print(f"{file}.csv: +{n} baris -> {len(rows)}")

# ------------------------------------------------ Facebook
header, rows = baca("facebook_propeaagency")
ada = {r["id"] for r in rows}
n = 0
for x in raw["facebook"]:
    if x["id"] in ada:
        continue
    baris = {
        "id": x["id"], "platform": "facebook", "akun": x["akun"], "url": x["url"],
        "teks": x["teks"], "likes": "", "komentar": x.get("komentar", ""),
        "share": x.get("share", ""), "views": "", "format": x.get("format", "foto"),
    }
    baris.update(basis(x["teks"], x["tanggal"]))
    baris["engagement"] = ""
    baris["er_views"] = ""
    rows.append({**{h: "" for h in header}, **baris})
    tambahan["@propeaagency (facebook)"] += 1
    ada.add(x["id"])
    n += 1
tulis("facebook_propeaagency", header, rows)
print(f"facebook_propeaagency.csv: +{n} baris -> {len(rows)}")

# ------------------------------------------------ Ringkasan akun
for r in rows_ring:
    if r["akun"] in tambahan and tambahan[r["akun"]]:
        r["post"] = str(int(float(r["post"] or 0)) + tambahan[r["akun"]])
tulis("ringkasan_akun", header_ring, rows_ring)
print("Ringkasan akun diperbarui:", {k: v for k, v in tambahan.items() if v})
print("Selesai. Jalankan ulang proses_winning.py hanya jika ingin menghitung ulang seluruh klasifikasi.")

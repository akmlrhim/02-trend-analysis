# -*- coding: utf-8 -*-
"""Dashboard riset tren konten. Data mentah: folder data/, diambil 6 Nov 2026."""
from datetime import timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Riset Tren Konten", layout="wide")

TGL_AMBIL = "6 Nov 2026"

# Palet: netral biru-abu sebagai dasar, satu aksen merah-bata untuk tren naik.
# Warna semantik dipakai hanya untuk sentimen dan status sumber.
NETRAL = "#3D5A6C"
AKSEN = "#C73E1D"
SENTIMEN = {"positif": "#5B8C5A", "netral": "#9AA0A6", "negatif": "#C73E1D"}
STATUS = {"berhasil": "#5B8C5A", "sebagian": "#D9A441", "gagal": "#C73E1D", "dilewati": "#B9BDC4"}
RELEVANSI = {"tinggi": "#C73E1D", "sedang": "#D9A441", "rendah": "#B9BDC4"}


@st.cache_data
def load_csv(name):
    return pd.read_csv(f"data/{name}", encoding="utf-8-sig", dtype=str).fillna("")


tren = load_csv("tren_topik.csv")
tanya = load_csv("pertanyaan_audiens.csv")
kalender = load_csv("kalender_momen.csv")
checklist = load_csv("_sumber_checklist.csv")
refkonten = load_csv("referensi_konten.csv")

for df in (tren, tanya):
    df["tanggal_ambil"] = pd.to_datetime(df["tanggal_ambil"], errors="coerce")
kalender["tanggal_dt"] = pd.to_datetime(kalender["tanggal"], errors="coerce")
checklist["jumlah_baris"] = pd.to_numeric(checklist["jumlah_baris"], errors="coerce")

halaman = st.sidebar.radio(
    "Navigasi",
    ["Ringkasan", "Tren Topik", "Pertanyaan Audiens", "Kalender Momen", "Acuan Konten", "Sumber & Checklist"],
)
st.sidebar.markdown("---")
st.sidebar.caption(f"Industri: agensi digital marketing / jasa digital. Data diambil {TGL_AMBIL}. File mentah ada di folder data/.")


def barh(df, kolom, pertanyaan, warna=NETRAL):
    """Bar horizontal: judulnya pertanyaan yang dijawab chart."""
    vc = df[kolom].value_counts().reset_index()
    vc.columns = [kolom, "jumlah"]
    fig = px.bar(vc.sort_values("jumlah"), x="jumlah", y=kolom, orientation="h",
                 title=pertanyaan, color_discrete_sequence=[warna], text="jumlah")
    fig.update_layout(height=max(320, 26 * len(vc) + 90),
                      yaxis_title="", xaxis_title="jumlah baris",
                      margin=dict(l=10, r=10, t=42, b=10))
    fig.update_traces(textposition="outside")
    return fig


def pie_sentimen(df):
    vc = df["sentimen"].value_counts().reindex(["positif", "netral", "negatif"]).dropna().reset_index()
    vc.columns = ["sentimen", "jumlah"]
    fig = px.pie(vc, names="sentimen", values="jumlah", hole=0.45,
                 title="Sebagian besar topik bersentimen apa?",
                 color="sentimen", color_discrete_map=SENTIMEN)
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=42, b=10))
    return fig


if halaman == "Ringkasan":
    st.title("Yang sedang hangat di Indonesia")
    st.caption(f"Industri owner: agensi digital marketing / jasa digital. Data diambil {TGL_AMBIL}, geo Indonesia.")

    st.markdown(
        f"Dataset berisi **{len(tren)} baris tren** dari {tren['sumber'].nunique()} sumber, "
        f"**{len(tanya)} pertanyaan audiens**, dan **{len(kalender)} momen** untuk 60 hari ke depan. "
        f"Dari {len(checklist)} sumber yang dicoba, {int((checklist['status'] == 'berhasil').sum())} berhasil penuh."
    )

    st.markdown("### Lima isu industri yang paling relevan")
    hangat = tren[(tren["kategori"].isin(["industri_digital", "media_sosial", "e_commerce", "teknologi", "internet_budaya"]))
                  & (tren["indikator_tren"] == "naik")].head(5)
    for _, r in hangat.iterrows():
        st.markdown(f"- **{r['topik']}** ({r['kategori'].replace('_', ' ')})")

    a, b = st.columns([3, 2])
    with a:
        st.plotly_chart(barh(tren, "kategori", "Kategori apa yang paling banyak dibahas?"),
                        width='stretch')
    with b:
        st.plotly_chart(pie_sentimen(tren), width='stretch')

    st.plotly_chart(barh(tren, "indikator_tren", "Berapa banyak tren yang masih naik, dibanding stabil atau turun?", AKSEN),
                    width='stretch')

elif halaman == "Tren Topik":
    st.title("Tren Topik")
    st.caption("Pilih kategori dan sentimen untuk mempersempit topik yang naik.")

    f1, f2, f3 = st.columns(3)
    kat = f1.multiselect("Kategori", sorted(tren["kategori"].unique()),
                         default=sorted(tren["kategori"].unique())[:8])
    sen = f2.multiselect("Sentimen", sorted(tren["sentimen"].unique()),
                         default=sorted(tren["sentimen"].unique()))
    ind = f3.multiselect("Arah tren", sorted(tren["indikator_tren"].unique()),
                         default=sorted(tren["indikator_tren"].unique()))
    d = tren[tren["kategori"].isin(kat) & tren["sentimen"].isin(sen) & tren["indikator_tren"].isin(ind)]

    if d.empty:
        st.info("Tidak ada baris yang cocok dengan filter ini. Longgarkan pilihan kategori atau sentimen di atas.")
    else:
        a, b = st.columns(2)
        with a:
            st.plotly_chart(barh(d, "kategori", f"Kategori mana yang paling banyak? ({len(d)} baris)"),
                            width='stretch')
        with b:
            st.plotly_chart(barh(d, "sumber", "Sumber mana yang paling produktif?", NETRAL),
                            width='stretch')

        st.markdown("### Topik yang sedang naik")
        naik = d[d["indikator_tren"] == "naik"]
        if naik.empty:
            st.info("Tidak ada topik berindikator naik pada filter ini.")
        else:
            st.dataframe(naik[["kategori", "topik", "kata_kunci", "skor_atau_volume", "sentimen", "sumber", "source_url"]],
                         width='stretch', height=380)

        with st.expander("Semua baris dataset 1"):
            st.dataframe(d[["kategori", "topik", "kata_kunci", "sumber", "indikator_tren",
                            "skor_atau_volume", "sentimen", "source_url"]],
                         width='stretch', height=480)

elif halaman == "Pertanyaan Audiens":
    st.title("Pertanyaan Audiens")
    st.caption("Pertanyaan dan keluhan yang benar-benar dicari orang, untuk menentukan topik konten yang menjawabnya.")

    f1, f2 = st.columns(2)
    kat = f1.multiselect("Kategori", sorted(tanya["kategori"].unique()),
                         default=sorted(tanya["kategori"].unique())[:10])
    src = f2.multiselect("Sumber", sorted(tanya["sumber"].unique()),
                         default=sorted(tanya["sumber"].unique()))
    d = tanya[tanya["kategori"].isin(kat) & tanya["sumber"].isin(src)]

    if d.empty:
        st.info("Tidak ada pertanyaan yang cocok dengan filter ini. Coba tambahkan kategori atau sumber.")
    else:
        a, b = st.columns(2)
        with a:
            st.plotly_chart(barh(d, "kategori", f"Topik apa yang paling sering ditanyakan? ({len(d)} baris)", NETRAL),
                            width='stretch')
        with b:
            st.plotly_chart(barh(d, "sumber", "Dari sumber mana pertanyaan itu datang?"),
                            width='stretch')

        st.markdown(f"### Daftar pertanyaan ({len(d)} baris)")
        st.dataframe(d[["kategori", "pertanyaan_atau_keluhan", "sumber",
                        "frekuensi_atau_jumlah_mention", "source_url"]],
                     width='stretch', height=460)

elif halaman == "Kalender Momen":
    st.title("Kalender Momen 60 Hari")
    st.caption("Momen yang layak disiapkan lebih awal, dari 7 Nov 2026 sampai 5 Jan 2027. Warna menunjukkan relevansi.")

    f1, f2 = st.columns(2)
    jenis = f1.multiselect("Jenis momen", sorted(kalender["jenis"].unique()),
                           default=sorted(kalender["jenis"].unique()))
    rel = f2.multiselect("Relevansi", ["tinggi", "sedang", "rendah"], default=["tinggi", "sedang", "rendah"])
    d = kalender[kalender["jenis"].isin(jenis) & kalender["relevansi"].isin(rel)].copy()
    d = d.sort_values("tanggal_dt")

    if d.empty:
        st.info("Tidak ada momen pada filter ini. Pilih jenis atau relevansi lain.")
    else:
        d["akhir"] = d["tanggal_dt"] + timedelta(days=1)
        fig = px.timeline(d, x_start="tanggal_dt", x_end="akhir", y="nama_momen",
                          color="relevansi", color_discrete_map=RELEVANSI,
                          category_orders={"relevansi": ["tinggi", "sedang", "rendah"]},
                          title=f"Momen apa saja dalam 60 hari ke depan? ({len(d)} momen)")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=max(420, 26 * len(d) + 100), margin=dict(l=10, r=10, t=42, b=10))
        st.plotly_chart(fig, width='stretch')

        a, b = st.columns(2)
        with a:
            st.plotly_chart(barh(d, "jenis", "Jenis momen apa yang paling banyak?"), width='stretch')
        with b:
            tinggi = d[d["relevansi"] == "tinggi"]
            st.markdown(f"### Prioritas tinggi ({len(tinggi)} momen)")
            for _, r in tinggi.iterrows():
                st.markdown(f"- **{r['tanggal']}**: {r['nama_momen']}")

        st.markdown("### Daftar lengkap")
        st.dataframe(d[["tanggal", "nama_momen", "jenis", "relevansi", "catatan", "source_url"]],
                     width='stretch', height=420)

elif halaman == "Acuan Konten":
    st.title("Acuan Konten")
    st.caption(f"Pemetaan isu terverifikasi menjadi sudut konten siap produksi. Dibuat {TGL_AMBIL}; setiap baris terhubung ke sumber datanya.")

    f1, f2 = st.columns(2)
    kat = f1.multiselect("Kategori", sorted(refkonten["kategori"].unique()), default=sorted(refkonten["kategori"].unique()))
    fmt = f2.multiselect("Format", sorted(refkonten["format_saran"].unique()), default=sorted(refkonten["format_saran"].unique()))
    d = refkonten[refkonten["kategori"].isin(kat) & refkonten["format_saran"].isin(fmt)]

    st.markdown(
        f"**{len(d)} sudut konten** siap produksi. Yang paling mendesak: isu iklan silang Meta-TikTok dan "
        "kampanye Harbolnas 12.12, karena keduanya punya batas waktu."
    )

    st.plotly_chart(barh(d, "format_saran", "Format konten apa yang paling banyak disarankan?", NETRAL),
                    width='stretch')

    st.markdown("### Daftar sudut konten")
    st.dataframe(d[["kategori", "isu_data", "sudut_konten", "format_saran", "momen_kalender", "sumber_data", "source_url"]],
                 width='stretch', height=480)

    berjeda = d[d["momen_kalender"] != "-"]
    if not berjeda.empty:
        st.markdown("### Punya batas waktu (terkait momen kalender)")
        for _, r in berjeda.iterrows():
            st.markdown(f"- **{r['momen_kalender']}**: {r['sudut_konten']}")

else:
    st.title("Sumber & Checklist")
    st.caption("Satu baris per sumber wajib, termasuk tiap bagian Google Trends. Status gagal disertai alasannya.")

    ds = st.selectbox("Dataset", sorted(checklist["dataset"].unique()))
    d = checklist[checklist["dataset"] == ds]

    st.markdown(
        f"Dataset {ds}: **{int((d['status'] == 'berhasil').sum())} berhasil**, "
        f"{int((d['status'] == 'sebagian').sum())} sebagian, "
        f"{int((d['status'] == 'gagal').sum())} gagal, "
        f"{int((d['status'] == 'dilewati').sum())} dilewati."
    )

    fig = px.bar(d.sort_values("jumlah_baris"), x="jumlah_baris", y="sumber", orientation="h",
                 color="status", text="jumlah_baris", color_discrete_map=STATUS,
                 category_orders={"status": ["berhasil", "sebagian", "gagal", "dilewati"]},
                 title="Sumber mana yang berhasil, dan mana yang tidak?")
    fig.update_layout(height=max(360, 30 * len(d) + 100), margin=dict(l=10, r=10, t=42, b=10))
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, width='stretch')

    st.markdown("### Rincian per sumber")
    st.dataframe(d[["sumber", "status", "jumlah_baris", "tool_yang_dipakai", "alasan_jika_gagal"]],
                 width='stretch', height=420)

st.sidebar.markdown("---")
st.sidebar.caption("Data mentah untuk perencanaan konten, bukan ide konten jadi.")

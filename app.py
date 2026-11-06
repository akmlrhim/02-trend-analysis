# -*- coding: utf-8 -*-
"""Dashboard riset konten Impost Media. Data mentah: folder data/, riset terakhir 6 Nov 2026."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Riset Konten Impost Media", layout="wide")

TGL_AMBIL = "6 Nov 2026"
PERIODE = "7 Okt - 6 Nov 2026"

# Palet: netral biru-abu sebagai dasar, satu aksen merah-bata untuk tren naik.
NETRAL = "#3D5A6C"
AKSEN = "#C73E1D"
SENTIMEN = {"positif": "#5B8C5A", "netral": "#9AA0A6", "negatif": "#C73E1D"}
STATUS = {"berhasil": "#5B8C5A", "sebagian": "#D9A441", "gagal": "#C73E1D", "dilewati": "#B9BDC4"}
KEYAKINAN = {"tinggi": "#5B8C5A", "sedang": "#D9A441", "rendah": "#C73E1D"}
URGENSI = {"tinggi": "#C73E1D", "sedang": "#D9A441", "rendah": "#B9BDC4"}


@st.cache_data(ttl="1h")  # muat ulang otomatis tiap 1 jam agar tidak menyajikan data lama
def load_csv(name):
    return pd.read_csv(f"data/{name}", encoding="utf-8-sig", dtype=str).fillna("")


tren = load_csv("tren_topik.csv")
tanya = load_csv("pertanyaan_audiens.csv")
checklist = load_csv("_sumber_checklist.csv")
isu = load_csv("isu_impost.csv")
ide = load_csv("ide_konten_impost.csv")

for df in (tren, tanya):
    df["tanggal_ambil"] = pd.to_datetime(df["tanggal_ambil"], errors="coerce")
checklist["jumlah_baris"] = pd.to_numeric(checklist["jumlah_baris"], errors="coerce")

halaman = st.sidebar.radio(
    "Navigasi",
    ["Ringkasan", "Isu & Ide Konten", "Tren Topik",
     "Pertanyaan Audiens", "Sumber & Checklist"],
)
st.sidebar.markdown("---")
if st.sidebar.button("Muat ulang data", icon=":material/refresh:", key="btn_refresh_data"):
    st.cache_data.clear()
    st.rerun()
st.sidebar.caption(f"Riset untuk Impost Media (impostmedia.com), agensi digital marketing Kalsel. "
                   f"Periode data {PERIODE}. Riset terakhir {TGL_AMBIL}.")


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


def badge(label, warna):
    return f'<span style="background:{warna};color:white;padding:2px 10px;border-radius:12px;font-size:0.8em">{label}</span>'


# ============ RINGKASAN ============
if halaman == "Ringkasan":
    st.title("Riset Konten Impost Media")
    st.caption(f"Periode riset {PERIODE}. Disusun {TGL_AMBIL} untuk pemilik bisnis Kalsel & Indonesia - bahasa awam, semua klaim bersumber.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Isu terpilih", f"{len(isu)}", f"{int((isu['urgensi'] == 'tinggi').sum())} urgensi tinggi")
    c2.metric("Ide konten siap produksi", len(ide))
    c3.metric("Baris tren terkurasi", len(tren))

    st.markdown("### 5 isu terpilih (validasi 2+ sumber)")
    for _, r in isu.sort_values("prioritas").iterrows():
        st.markdown(
            f"**{int(r['prioritas'])}. {r['judul']}**  \n"
            f"{badge('urgensi: ' + r['urgensi'], URGENSI.get(r['urgensi'], NETRAL))} "
            f"{badge('keyakinan: ' + r['keyakinan'], KEYAKINAN.get(r['keyakinan'], NETRAL))} "
            f"{badge('layanan: ' + r['layanan_relevan'], NETRAL)}",
            unsafe_allow_html=True,
        )

    a, b = st.columns([3, 2])
    with a:
        st.plotly_chart(barh(tren, "kategori", "Data pendukung paling banyak dari kategori mana?"),
                        width='stretch')
    with b:
        st.plotly_chart(pie_sentimen(tren), width='stretch')

    st.plotly_chart(barh(tren, "indikator_tren",
                         "Berapa banyak tren yang masih naik, dibanding stabil atau turun?", AKSEN),
                    width='stretch')

# ============ ISU & IDE KONTEN ============
elif halaman == "Isu & Ide Konten":
    st.title("Isu & Ide Konten")
    st.caption("Tiap isu tervalidasi 2+ sumber independen, lalu diubah jadi ide konten IG/TikTok siap produksi.")

    pilihan = st.selectbox("Pilih isu", isu.sort_values("prioritas")["judul"], index=0)
    r = isu[isu["judul"] == pilihan].iloc[0]
    d_ide = ide[ide["id_isu"] == r["id_isu"]]

    st.markdown(
        f"### {r['judul']}  \n"
        f"{badge('urgensi: ' + r['urgensi'], URGENSI.get(r['urgensi'], NETRAL))} "
        f"{badge('keyakinan: ' + r['keyakinan'], KEYAKINAN.get(r['keyakinan'], NETRAL))} "
        f"{badge('prioritas: ' + str(int(float(r['prioritas']))), NETRAL)}",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ringkasan", "Mengapa penting", "Data pendukung",
                                            "Sudut unik", "Layanan & sumber"])
    with tab1:
        st.write(r["ringkasan"])
    with tab2:
        st.write(r["mengapa_peduli"])
    with tab3:
        st.write(r["data_pendukung"])
        st.markdown(f"Sumber utama: [{r['sumber_utama']}]({r['source_url']})")
    with tab4:
        st.write(r["sudut_unik"])
    with tab5:
        st.markdown(f"**Layanan Impost Media yang relevan:** {r['layanan_relevan']}")

    st.markdown(f"### Ide konten ({len(d_ide)})")
    for _, i in d_ide.iterrows():
        with st.expander(f"{i['platform']} - {i['format']}: **{i['nama_ide']}**"):
            st.markdown(f"**Hook / slide pertama:**  \n> {i['hook']}")
            st.markdown("**Poin isi:**")
            for p in i["poin_isi"].split("|"):
                st.markdown(f"- {p.strip()}")
            st.markdown(f"**CTA:** {i['cta']}")
            st.caption(f"Visual & audio: {i['visual_audio']}")

    st.plotly_chart(barh(ide, "platform", "Ide terdistribusi ke platform apa?"), width='stretch')

# ============ TREN TOPIK ============
elif halaman == "Tren Topik":
    st.title("Tren Topik")
    st.caption(f"Dataset terkurasi hasil riset {TGL_AMBIL}: hanya tren tervalidasi sumber, tanpa tren sekena. Pilih kategori dan sentimen untuk mempersempit.")

    f1, f2, f3 = st.columns(3)
    kat = f1.multiselect("Kategori", sorted(tren["kategori"].unique()),
                         default=sorted(tren["kategori"].unique()))
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

        with st.expander("Semua baris dataset"):
            st.dataframe(d[["kategori", "topik", "kata_kunci", "sumber", "indikator_tren",
                            "skor_atau_volume", "sentimen", "source_url"]],
                         width='stretch', height=480)

# ============ PERTANYAAN AUDIENS ============
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

# ============ SUMBER & CHECKLIST ============
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
st.sidebar.caption("Riset: isu terverifikasi -> ide konten siap produksi. Data lama diarsipkan di data/_arsip/.")

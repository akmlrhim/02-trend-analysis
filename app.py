# -*- coding: utf-8 -*-
"""Dashboard riset konten Impost Media. Data mentah: folder data/, riset terakhir 6 Nov 2026."""
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
import subprocess
import sys

st.set_page_config(page_title="Riset Konten Impost Media", layout="wide")

ROOT = Path(__file__).parent
# Fallback bila kolom tanggal_ambil kosong/tak terbaca
TGL_AMBIL = "6 Nov 2026"
PERIODE = "7 Okt - 6 Nov 2026"


def fmt_tgl(dt):
    """'6 Nov 2026' tanpa nol depan, aman lintas OS."""
    return f"{dt.day} {dt.strftime('%b %Y')}"

# Palet: netral biru-abu sebagai dasar, satu aksen merah-bata untuk tren naik.
NETRAL = "#3D5A6C"
AKSEN = "#C73E1D"


def _mtime(name):
    """Timestamp file CSV; dipakai sebagai argumen cache supaya data baru
    langsung termuat tanpa menunggu ttl, begitu file di-update pipeline."""
    try:
        return Path(f"data/{name}").stat().st_mtime
    except OSError:
        return 0.0


@st.cache_data(ttl="1h")  # muat ulang otomatis tiap 1 jam atau saat file CSV berubah
def load_csv(name, mtime):
    return pd.read_csv(f"data/{name}", encoding="utf-8-sig", dtype=str).fillna("")


tren = load_csv("tren_topik.csv", _mtime("tren_topik.csv"))

tren["tanggal_ambil"] = pd.to_datetime(tren["tanggal_ambil"], errors="coerce")
# Tanggal riset & periode mengikuti data terbaru di CSV, bukan angka hardcoded
if tren["tanggal_ambil"].notna().any():
    tgl_min = tren["tanggal_ambil"].min()
    tgl_max = tren["tanggal_ambil"].max()
    PERIODE = fmt_tgl(tgl_min) if tgl_min == tgl_max else f"{fmt_tgl(tgl_min)} - {fmt_tgl(tgl_max)}"
    TGL_AMBIL = fmt_tgl(tgl_max)

halaman = st.sidebar.radio(
    "Navigasi",
    ["Tren Topik", "Konten Winning"],
)
st.sidebar.markdown("---")
if st.sidebar.button("Muat ulang data", icon=":material/refresh:", key="btn_refresh_data"):
    st.cache_data.clear()
    st.rerun()
st.sidebar.caption(f"Riset untuk Impost Media (impostmedia.com), agensi digital marketing Kalsel. "
                   f"Periode data {PERIODE}. Riset terakhir {TGL_AMBIL}.")


def tombol_ambil_data():
    """Tombol + status pengambilan data terbaru, ditampilkan di atas tiap halaman."""
    with st.container(horizontal=True, horizontal_alignment="right"):
        klik = st.button("Ambil data terbaru", icon=":material/cloud_download:", key="btn_fetch_data")
    if klik:
        # Jalankan refresh_weekly.py: pytrends, X trending, berita industri, TikTok trending,
        # lalu tambah baris baru ke CSV (dengan dedupe) dan normalisasi format.
        with st.status("Mengambil data terbaru...", expanded=True) as status:
            st.write("Menjalankan scripts/refresh_weekly.py (pytrends, X, berita, TikTok)...")
            try:
                proses = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "refresh_weekly.py")],
                    cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=900,
                )
                st.code((proses.stdout + "\n" + proses.stderr).strip() or "(tanpa output)")
                if proses.returncode == 0:
                    status.update(label="Data terbaru berhasil diambil", state="complete", expanded=False)
                    st.cache_data.clear()
                    st.toast("Data terbaru dimuat", icon=":material/check_circle:")
                    st.rerun()
                else:
                    status.update(label="Pengambilan data gagal, lihat log", state="error")
            except subprocess.TimeoutExpired:
                status.update(label="Proses melebihi 15 menit, dihentikan", state="error")


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


# ============ TREN TOPIK ============
if halaman == "Tren Topik":
    st.title("Tren Topik")
    tombol_ambil_data()
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

# ============ KONTEN WINNING ============
elif halaman == "Konten Winning":
    st.title("Analisa Konten Winning")
    tombol_ambil_data()
    st.caption(
        "Data post asli @impostmedia (TikTok & Instagram), @impeeps.ofc (akun Gen Z Impost), "
        f"dan halaman Facebook @propeaagency, diambil {TGL_AMBIL} via Apify. "
        "TikTok: 225 post Feb 2025-Okt 2026. FB: 236 post Mar 2025-Okt 2026. "
        "Winning = post di kuartil atas (top 25%) performa akunnya sendiri; losing = kuartil bawah."
    )

    @st.cache_data(ttl="1h")
    def load_winning_csv(name, mtime):
        return pd.read_csv(f"data/konten_winning/{name}", encoding="utf-8-sig")

    tt_win = load_winning_csv("tiktok_impostmedia.csv", _mtime("konten_winning/tiktok_impostmedia.csv"))
    ig_win = load_winning_csv("instagram_impostmedia.csv", _mtime("konten_winning/instagram_impostmedia.csv"))
    ig_peeps = load_winning_csv("instagram_impeeps.csv", _mtime("konten_winning/instagram_impeeps.csv"))
    fb_win = load_winning_csv("facebook_propeaagency.csv", _mtime("konten_winning/facebook_propeaagency.csv"))
    ringkas = load_winning_csv("ringkasan_akun.csv", _mtime("konten_winning/ringkasan_akun.csv"))

    # --- KPI akun
    st.markdown("### Profil aset akun Impost Media")
    k = ringkas.set_index("akun")

    def post_dan_winning(akun):
        """Angka post & winning dari ringkasan; 0 bila baris belum ada (mis. cache/data lama)."""
        if akun in k.index:
            return int(k.loc[akun, "post"]), int(k.loc[akun, "winning"])
        return 0, 0

    m1, m2, m3, m4, m5 = st.columns(5)
    tt_post, tt_win_n = post_dan_winning("@impostmedia")
    m1.metric("TikTok @impostmedia", f"{tt_post} post", f"{tt_win_n} winning · 177 followers")
    ig_post, ig_win_n = post_dan_winning("@impostmedia (utama)")
    m2.metric("IG @impostmedia (utama)", f"{ig_post} post", "17.588 followers")
    kol_post, _ = post_dan_winning("@impostmedia (kolab impeeps)")
    m3.metric("IG @impostmedia (kolab impeeps)", f"{kol_post} reels", "like puncak 243.285")
    peps_post, peps_win_n = post_dan_winning("@impeeps.ofc")
    m4.metric("IG @impeeps.ofc", f"{peps_post} post", f"{peps_win_n} winning · 553 followers")
    fb_post, fb_win_n = post_dan_winning("@propeaagency (facebook)")
    m5.metric("FB @propeaagency", f"{fb_post} post", f"{fb_win_n} winning")

    tab_tt, tab_ig, tab_fb, tab_top, tab_mtd = st.tabs(
        ["TikTok", "Instagram", "Facebook", "Daftar konten winning", "Metodologi"])

    # ---------------- TIKTOK ----------------
    with tab_tt:
        st.markdown("#### TikTok @impostmedia — apa yang bikin post masuk top 25%?")

        a1, a2 = st.columns(2)
        with a1:
            vc = tt_win["status"].value_counts().reindex(["WINNING", "normal", "losing"]).fillna(0).reset_index()
            vc.columns = ["status", "jumlah"]
            fig = px.bar(vc, x="status", y="jumlah", color="status",
                         color_discrete_map={"WINNING": AKSEN, "normal": NETRAL, "losing": "#B9BDC4"},
                         title="Seberapa banyak post yang winning?", text="jumlah")
            fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with a2:
            agg = tt_win.groupby("topik").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            agg = agg.sort_values("median_views")
            fig = px.bar(agg, x="median_views", y="topik", orientation="h",
                         color_discrete_sequence=[NETRAL], text="median_views",
                         title="Topik mana yang paling banyak dilihat? (median views)")
            fig.update_traces(textposition="outside")
            fig.update_layout(height=360, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')

        b1, b2 = st.columns(2)
        with b1:
            agg = tt_win.groupby("format").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            fig = px.bar(agg, x="format", y="median_views", color="format",
                         color_discrete_map={"slideshow": AKSEN, "video": NETRAL}, text="median_views",
                         title="Slideshow 2,8x lebih banyak dilihat daripada video")
            fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with b2:
            urut_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
            agg = tt_win.groupby("hari").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            agg["hari"] = pd.Categorical(agg["hari"], urut_hari, ordered=True)
            agg = agg.sort_values("hari")
            fig = px.bar(agg, x="hari", y="median_views", color_discrete_sequence=[NETRAL], text="median_views",
                         title="Hari apa posting paling banyak dilihat? (median views)")
            fig.update_traces(textposition="outside")
            fig.update_layout(height=360, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')

        c1, c2 = st.columns(2)
        with c1:
            pivot = tt_win.pivot_table(index="hari", columns="jam", values="views", aggfunc="median")
            pivot = pivot.reindex(urut_hari)
            fig = px.imshow(pivot, aspect="auto", color_continuous_scale="OrRd",
                            title="Kapan waktu posting paling 'panas'? (median views hari x jam WITA)",
                            labels=dict(x="jam (WITA)", y="hari", color="median views"))
            fig.update_layout(height=380, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with c2:
            tt_win["bulan"] = pd.to_datetime(tt_win["tanggal"]).dt.strftime("%Y-%m")
            agg = tt_win.groupby("bulan").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            fig = px.line(agg, x="bulan", y="median_views", markers=True, color_discrete_sequence=[AKSEN],
                          title="Arah performa akun: median views per bulan (naik, tapi frekuensi turun)")
            fig.update_layout(height=380, margin=dict(l=10, r=10, t=42, b=10),
                              xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')

        d1, d2 = st.columns(2)
        with d1:
            tt_win["htag_n"] = tt_win["hashtags"].where(tt_win["hashtags"].notna(), "").apply(lambda s: len([h for h in str(s).split(",") if h.strip()]))
            tt_win["htag_bin"] = pd.cut(tt_win["htag_n"], [-1, 1, 3, 5, 50], labels=["0-1", "2-3", "4-5", ">5"])
            agg = tt_win.groupby("htag_bin", observed=True).agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            fig = px.bar(agg, x="htag_bin", y="median_views", color_discrete_sequence=[NETRAL], text="median_views",
                         title="Berapa jumlah hashtag optimal? (median views)")
            fig.update_layout(height=340, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with d2:
            tt_win["tag_brand"] = tt_win["hashtags"].where(tt_win["hashtags"].notna(), "").str.lower().str.contains("impostmedia")
            agg = tt_win.groupby("tag_brand").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            agg["tag_brand"] = agg["tag_brand"].map({True: "pakai #impostmedia", False: "tanpa #impostmedia"})
            fig = px.bar(agg, x="tag_brand", y="median_views", color="tag_brand",
                         color_discrete_map={"pakai #impostmedia": AKSEN, "tanpa #impostmedia": "#B9BDC4"},
                         text="median_views", title="Post dengan tag brand #impostmedia = 2x views")
            fig.update_layout(height=340, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')

        st.markdown("#### 15 konten TikTok winning teratas")
        top_tt = tt_win.nlargest(15, "views")[
            ["tanggal_jakarta", "views", "likes", "komentar", "share", "simpan", "er_views", "format", "topik", "teks", "url"]
        ].copy()
        top_tt["teks"] = top_tt["teks"].astype(str).str.slice(0, 90) + "..."
        top_tt.columns = ["tanggal", "views", "likes", "komentar", "share", "simpan", "ER %", "format", "topik", "cuplikan teks", "url"]
        st.dataframe(top_tt, width='stretch', height=420)

    # ---------------- INSTAGRAM ----------------
    with tab_ig:
        st.markdown("#### Instagram — konten siapa yang winning?")

        seg = ig_win[["segmen", "engagement", "likes", "komentar"]].copy()
        seg["akun_label"] = seg["segmen"].map({"akun_utama": "@impostmedia (konten korporat)",
                                               "kolab_impeeps": "@impostmedia (kolaborasi @impeeps.ofc)"})
        peeps = ig_peeps[["engagement", "likes", "komentar"]].copy()
        peeps["akun_label"] = "@impeeps.ofc (konten Gen Z agency)"
        semua = pd.concat([seg[["akun_label", "engagement", "likes", "komentar"]], peeps])

        agg = semua.groupby("akun_label").agg(median_engagement=("engagement", "median"),
                                              n=("engagement", "size")).reset_index()
        fig = px.bar(agg, x="akun_label", y="median_engagement", color="akun_label",
                     color_discrete_map={"@impostmedia (konten korporat)": "#B9BDC4",
                                         "@impostmedia (kolaborasi @impeeps.ofc)": AKSEN,
                                         "@impeeps.ofc (konten Gen Z agency)": NETRAL},
                     text="median_engagement",
                     title="Median engagement per jenis akun — siapa mesin winning-nya?")
        fig.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
        st.plotly_chart(fig, width='stretch')

        sub_utm, sub_peeps = st.tabs(["@impostmedia", "@impeeps.ofc"])

        # ------- @impostmedia (akun utama & kolaborasi) -------
        with sub_utm:
            utama = ig_win[ig_win["segmen"] == "akun_utama"]
            kom = utama[utama["komentar"] > 0].nlargest(10, "komentar")[
                ["tanggal_jakarta", "format", "topik", "likes", "komentar", "teks", "url"]].copy()
            kom["teks"] = kom["teks"].astype(str).str.slice(0, 60) + "..."
            kom.columns = ["tanggal", "format", "topik", "likes", "komentar", "cuplikan teks", "url"]
            st.markdown("##### 10 post akun utama paling banyak dikomentari")
            st.dataframe(kom, width='stretch', height=380)
            st.info(
                "Catatan: 73% post IG menyembunyikan jumlah like (fitur Instagram), jadi median engagement tampil rendah. "
                "Sinyal paling adil: komentar. Akun utama median komentar **0**; konten yang paling banyak dikomentari justru "
                "konten rekrutmen (loker video editor: 12 komentar) — sementara reels kolaborasi @impeeps.ofc menembus "
                "ratusan ribu like."
            )

        # ------- @impeeps.ofc (akun Gen Z) -------
        with sub_peeps:
            p1, p2 = st.columns(2)
            with p1:
                vc = ig_peeps["status"].value_counts().reindex(["WINNING", "normal", "losing"]).fillna(0).reset_index()
                vc.columns = ["status", "jumlah"]
                fig = px.bar(vc, x="status", y="jumlah", color="status",
                             color_discrete_map={"WINNING": AKSEN, "normal": NETRAL, "losing": "#B9BDC4"},
                             title="Seberapa banyak reels @impeeps.ofc yang winning?", text="jumlah")
                fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
                st.plotly_chart(fig, width='stretch')
            with p2:
                viral = ig_peeps.nlargest(8, "likes")[["likes", "komentar", "teks", "url"]].copy()
                viral["teks"] = viral["teks"].fillna("(caption tidak tersimpan)").astype(str).str.slice(0, 60) + "..."
                fig = px.bar(viral.sort_values("likes"), x="likes", y="teks", orientation="h",
                             color_discrete_sequence=[AKSEN], text="likes",
                             title="8 reels @impeeps.ofc paling viral (dari akun 553 followers)")
                fig.update_layout(height=360, margin=dict(l=10, r=10, t=42, b=10),
                                  yaxis_title="", xaxis_title="likes")
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig, width='stretch')

            q1, q2 = st.columns(2)
            with q1:
                urut_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                vc = ig_peeps["hari"].value_counts().reindex(urut_hari).fillna(0).reset_index()
                vc.columns = ["hari", "jumlah"]
                fig = px.bar(vc, x="hari", y="jumlah", color_discrete_sequence=[NETRAL], text="jumlah",
                             title="Hari apa @impeeps.ofc paling rajin posting? (jumlah post)")
                fig.update_layout(height=340, margin=dict(l=10, r=10, t=42, b=10))
                st.plotly_chart(fig, width='stretch')
            with q2:
                bulan_kom = (ig_peeps.assign(bulan=ig_peeps["tanggal_jakarta"].astype(str).str[:7])
                             .groupby("bulan")["komentar"].sum().reset_index())
                fig = px.bar(bulan_kom, x="bulan", y="komentar", color_discrete_sequence=[AKSEN],
                             title="Bulan apa yang paling banyak dikomentari? (total komentar)")
                fig.update_layout(height=340, margin=dict(l=10, r=10, t=42, b=10),
                                  xaxis_title="", yaxis_title="komentar", xaxis_tickangle=-45)
                st.plotly_chart(fig, width='stretch')

            kom_p = ig_peeps[ig_peeps["komentar"] > 0].nlargest(10, "komentar")[
                ["tanggal_jakarta", "likes", "komentar", "teks", "url"]].copy()
            kom_p["teks"] = kom_p["teks"].fillna("(caption tidak tersimpan)").astype(str).str.slice(0, 60) + "..."
            kom_p.columns = ["tanggal", "likes", "komentar", "cuplikan teks", "url"]
            st.markdown("##### 10 reels @impeeps.ofc paling banyak dikomentari")
            st.dataframe(kom_p, width='stretch', height=380)
            st.info(
                "Catatan: jumlah like @impeeps.ofc hanya tampil di 32 dari 180 post (sisanya disembunyikan IG), dan "
                "views reels tidak tersedia via scraper — jadi winning dihitung dari engagement (like terlihat + komentar). "
                "Caption kini terisi untuk 135 post hasil scrape ulang; median engagement per hari/bulan tidak ditampilkan "
                "karena nilainya 0 di hampir semua kelompok. Sinyal terbaik akun ini: **komentar** dan reels viralnya "
                "(243.285 like)."
            )

    # ---------------- FACEBOOK ----------------
    with tab_fb:
        st.markdown("#### Facebook @propeaagency — halaman FB resmi Impost Media")

        g1, g2 = st.columns(2)
        with g1:
            vc = fb_win["status"].value_counts().reindex(["WINNING", "normal", "losing", "tanpa_data"]).fillna(0).reset_index()
            vc.columns = ["status", "jumlah"]
            fig = px.bar(vc, x="status", y="jumlah", color="status",
                         color_discrete_map={"WINNING": AKSEN, "normal": NETRAL,
                                             "losing": "#B9BDC4", "tanpa_data": "#DDE1E4"},
                         title="Seberapa banyak post yang winning? (berdasar views)", text="jumlah")
            fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with g2:
            agg = fb_win.groupby("topik").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            agg = agg.sort_values("median_views")
            fig = px.bar(agg, x="median_views", y="topik", orientation="h",
                         color_discrete_sequence=[NETRAL], text="median_views",
                         title="Topik mana yang paling banyak dilihat? (median views)")
            fig.update_traces(textposition="outside")
            fig.update_layout(height=360, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')

        h1, h2 = st.columns(2)
        with h1:
            agg = fb_win[fb_win["format"] != "lainnya"].groupby("format").agg(
                median_views=("views", "median"), n=("views", "size")).reset_index()
            fig = px.bar(agg, x="format", y="median_views", color="format",
                         color_discrete_map={"reels": AKSEN, "video": NETRAL}, text="median_views",
                         title="Format mana yang paling banyak dilihat? (median views)")
            fig.update_layout(height=340, showlegend=False, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')
        with h2:
            urut_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
            agg = fb_win.groupby("hari").agg(median_views=("views", "median"), n=("views", "size")).reset_index()
            agg["hari"] = pd.Categorical(agg["hari"], urut_hari, ordered=True)
            agg = agg.sort_values("hari")
            fig = px.bar(agg, x="hari", y="median_views", color_discrete_sequence=[NETRAL], text="median_views",
                         title="Hari apa posting paling banyak dilihat? (median views)")
            fig.update_traces(textposition="outside")
            fig.update_layout(height=340, margin=dict(l=10, r=10, t=42, b=10))
            st.plotly_chart(fig, width='stretch')

        st.info(
            "Catatan: FB menyembunyikan jumlah like/komentar di hampir semua post (hanya 7 dari 236 post "
            "menampilkan angka like), jadi metrik utama halaman ini adalah **views** — dan itu hanya tersedia "
            "untuk post video/reels. Reach FB halaman ini kecil (median 9 views), tapi 1 reels jualan Desember 2025 "
            "menembus **27.186 views** — jauh di atas semua post lainnya."
        )

        st.markdown("#### 10 konten Facebook teratas")
        top_fb = fb_win.nlargest(10, "views")[
            ["tanggal_jakarta", "views", "likes", "share", "er_views", "format", "topik", "teks", "url"]
        ].copy()
        top_fb["teks"] = top_fb["teks"].astype(str).str.slice(0, 90) + "..."
        top_fb.columns = ["tanggal", "views", "likes", "share", "ER %", "format", "topik", "cuplikan teks", "url"]
        st.dataframe(top_fb, width='stretch', height=380)

    # ---------------- DAFTAR WINNING ----------------
    with tab_top:
        st.markdown("#### Semua konten WINNING (kuartil atas), bisa difilter")
        tt_w = tt_win[tt_win["status"] == "WINNING"][
            ["platform", "format", "topik", "views", "likes", "komentar", "er_views", "tanggal_jakarta", "teks", "url"]].copy()
        tt_w = tt_w.rename(columns={"er_views": "engagement_rate"})
        tt_w["akun"] = "@impostmedia"
        ig_w = ig_win[ig_win["status"] == "WINNING"][
            ["platform", "format", "topik", "views", "likes", "komentar", "segmen", "tanggal_jakarta", "teks", "url"]].copy()
        ig_w = ig_w.rename(columns={"segmen": "engagement_rate"})
        ig_w["engagement_rate"] = None
        ig_w["akun"] = "@impostmedia"
        peeps_w = ig_peeps[ig_peeps["status"] == "WINNING"][
            ["platform", "format", "topik", "views", "likes", "komentar", "engagement", "tanggal_jakarta", "teks", "url"]].copy()
        peeps_w = peeps_w.rename(columns={"engagement": "engagement_rate"})
        peeps_w["akun"] = "@impeeps.ofc"
        fb_w = fb_win[fb_win["status"] == "WINNING"][
            ["platform", "format", "topik", "views", "likes", "komentar", "tanggal_jakarta", "teks", "url"]].copy()
        fb_w["engagement_rate"] = None
        fb_w["akun"] = "@propeaagency"
        gab = pd.concat([tt_w, ig_w, peeps_w, fb_w], ignore_index=True)

        pl = st.multiselect("Platform", sorted(gab["platform"].unique()), default=sorted(gab["platform"].unique()))
        ak = st.multiselect("Akun", sorted(gab["akun"].unique()), default=sorted(gab["akun"].unique()))
        tk = st.multiselect("Topik", sorted(gab["topik"].unique()), default=sorted(gab["topik"].unique()))
        d = gab[gab["platform"].isin(pl) & gab["akun"].isin(ak) & gab["topik"].isin(tk)]
        d = d.assign(metrik=d["views"].fillna(d["likes"]).fillna(0)).sort_values("metrik", ascending=False)
        d["cuplikan"] = d["teks"].fillna("(caption tidak tersimpan)").astype(str).str.slice(0, 80) + "..."
        st.caption(f"{len(d)} konten winning dipilih. TikTok diurut views; IG diurut likes/komentar yang terlihat.")
        st.dataframe(
            d[["platform", "akun", "format", "topik", "views", "likes", "komentar", "engagement_rate", "tanggal_jakarta", "cuplikan", "url"]],
            width='stretch', height=520)

    # ---------------- METODOLOGI ----------------
    with tab_mtd:
        st.markdown("#### Cara baca halaman ini")
        st.markdown(
            "- **Winning** = post di kuartil atas (top 25%) metrik akunnya sendiri: TikTok memakai *views*, "
            "IG memakai *likes + komentar yang terlihat* (dihitung per segmen akun: utama / kolaborasi / @impeeps.ofc).\n"
            "- **Losing** = kuartil bawah (bottom 25%). Post IG yang menyembunyikan like dinilai dari komentar saja.\n"
            "- Waktu posting dikonversi ke WITA (Asia/Jakarta). Topik diklasifikasi otomatis dari caption "
            "(rekrutmen, hari besar, jualan klien, portfolio, edukasi, lainnya).\n"
            "- Sumber data: Apify `clockworks/tiktok-scraper`, `apify/instagram-scraper`, dan "
            f"`apify/facebook-posts-scraper`, diambil {TGL_AMBIL}. File: `data/konten_winning/`. "
            "Analisa lengkap: `analisis_konten_winning.md`.\n"
            "- Caption @impeeps.ofc berasal dari scrape ulang (`_raw/ig_impeeps_v2`, digabung per shortCode); "
            "post lama (Okt 2025-Jan 2026) tetap tanpa caption. Like @impeeps.ofc hanya tampil di 32 post dan views "
            "tidak tersedia, jadi winning dihitung dari engagement (like terlihat + komentar).\n"
            "- Facebook @propeaagency: winning dihitung dari **views** (FB menyembunyikan like/komentar di hampir semua "
            "post). Post foto/tekstual tanpa data views berstatus *tanpa_data*. Perbarui dengan "
            "`scripts/scraping/proses_winning_fb.py` setelah scrape ulang.\n"
            "- Untuk menyegarkan data TikTok/IG: jalankan ulang scraping Apify, taruh file mentah baru di "
            "`data/konten_winning/_raw/`, lalu jalankan `scripts/scraping/proses_winning.py`."
        )

st.sidebar.markdown("---")
st.sidebar.caption("Riset: tren terverifikasi & konten winning -> ide konten siap produksi. Data lama diarsipkan di data/_arsip/.")

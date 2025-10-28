import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ==============================
# BACA DATA
# ==============================
df = pd.read_excel("epidem.xlsx", index_col=0)

df["Jumlah Penduduk Total"] = df["Jumlah Penduduk Laki Laki"] + df["Jumlah Penduduk Perempuan"]
df["Jumlah Kasus Total"] = df["Jumlah Kasus Terkena DBD Laki Laki"] + df["Jumlah Kasus Terkena DBD Perempuan"]
df["Prevalensi DBD per 100.000"] = (df["Jumlah Kasus Total"] / df["Jumlah Penduduk Total"]) * 100000
df["Jumlah Kematian Total"] = df["Jumlah Kematian Karena DBD Laki Laki"] + df["Jumlah Kematian Karena DBD Perempuan"]
df["CFR DBD (%)"] = (df["Jumlah Kematian Total"] / df["Jumlah Kasus Total"]) * 100

# Prevalensi OR
prevalensi_OR = []
for _, row in df.iterrows():
    male_cases = row["Jumlah Kasus Terkena DBD Laki Laki"]
    female_cases = row["Jumlah Kasus Terkena DBD Perempuan"]
    male_pop = row["Jumlah Penduduk Laki Laki"]
    female_pop = row["Jumlah Penduduk Perempuan"]
    male_non = male_pop - male_cases
    female_non = female_pop - female_cases
    if female_cases == 0 or male_non == 0 or np.isnan(male_non) or np.isnan(female_non):
        OR = np.nan
    else:
        OR = (male_cases * female_non) / (female_cases * male_non)
    prevalensi_OR.append(OR)
df["Prevalensi OR (Laki-laki vs Perempuan)"] = prevalensi_OR

# =======================
# Agregat Provinsi Jawa Barat
# =======================

# Total kasus dan populasi
total_kasus = df["Jumlah Kasus Total"].sum()
total_penduduk = df["Jumlah Penduduk Total"].sum()

# Prevalensi DBD per 100.000 penduduk
prev_jabar = (total_kasus / total_penduduk) * 100000

# Total kematian dan CFR (Case Fatality Rate)
total_kematian = df["Jumlah Kematian Total"].sum()
cfr_jabar = (total_kematian / total_kasus) * 100

# =======================
# Odds Ratio (Laki-laki vs Perempuan) — Agregat Jawa Barat
# =======================

# Total kasus dan populasi berdasarkan jenis kelamin
kasus_laki = df["Jumlah Kasus Terkena DBD Laki Laki"].sum()
kasus_perempuan = df["Jumlah Kasus Terkena DBD Perempuan"].sum()
pop_laki = df["Jumlah Penduduk Laki Laki"].sum()
pop_perempuan = df["Jumlah Penduduk Perempuan"].sum()

# Non-kasus
non_laki = pop_laki - kasus_laki
non_perempuan = pop_perempuan - kasus_perempuan

# Hitung OR agregat Jawa Barat
or_jabar = (kasus_laki / non_laki) / (kasus_perempuan / non_perempuan)

# Nilai ekstrem
prev_max = df.loc[df["Prevalensi DBD per 100.000"].idxmax()]
prev_min = df.loc[df["Prevalensi DBD per 100.000"].idxmin()]
cfr_max = df.loc[df["CFR DBD (%)"].idxmax()]
cfr_min = df.loc[df["CFR DBD (%)"].idxmin()]
or_max = df.loc[df["Prevalensi OR (Laki-laki vs Perempuan)"].idxmax()]
or_min = df.loc[df["Prevalensi OR (Laki-laki vs Perempuan)"].idxmin()]

# =====================
# CSS FINAL — Responsif & Proporsional
# =====================
st.markdown(f"""
<h2 style="text-align:center; font-weight:800; margin-top:10px; margin-bottom:25px;">
Ukuran Statistik Epidemiologi Penyakit DBD Jawa Barat Tahun 2024
</h2>

<style>
/* ===== GRID UTAMA ===== */
.metric-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  justify-items: stretch;
  align-items: stretch;
  max-width: 1200px;
  margin: 0 auto 25px auto;
  padding: 0 15px;
}}

/* ===== BOX ===== */
.metric-box {{
  border-radius: 16px;
  # background-color: #ffffff;
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.25s ease;
  text-align: center;
}}
.metric-box:hover {{
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}}

/* ===== TEKS ===== */
.metric-title {{
  font-size: 17px;
  font-weight: 700;
  color: #FF4500;
  margin-bottom: 6px;
}}
.metric-value {{
  font-size: 34px;
  font-weight: 900;
  color: #FF0000;
  margin-bottom: 4px;
}}
.metric-sub {{
  color: #FF4500;
  font-size: 14px;
}}

/* ===== SUBDATA ===== */
.subrow {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 8px;
}}
.subcol-left, .subcol-right {{
  width: 48%;
}}
.subtitle {{
  font-size: 12px;
  font-weight: 700;
  color: #FF4500;
  margin-bottom: 2px;
}}
.subname {{
  font-size: 12px;
  font-weight: 600;
  color: #FF4500;
}}
.subvalue {{
  font-size: 13px;
  font-weight: 700;
  color: #FF4500;
}}

/* ===== RESPONSIVE ===== */
@media (max-width: 1100px) {{
  .metric-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}
}}
@media (max-width: 700px) {{
  .metric-grid {{
    grid-template-columns: 1fr;
  }}
  .metric-value {{
    font-size: 28px;
  }}
}}
</style>

<!-- ===== KONTEN KOTAK ===== -->
<div class="metric-grid">

  <div class="metric-box">
    <div class="metric-title">Total Kasus DBD</div>
    <div class="metric-value">{total_kasus:,.0f}</div>
    <div class="metric-sub">Jumlah seluruh kasus di Jawa Barat</div>
  </div>

  <div class="metric-box">
    <div class="metric-title">Prevalensi DBD per 100.000 Penduduk</div>
    <div class="metric-value">{prev_jabar:.2f}</div>
    <div class="subrow">
      <div class="subcol-left" style="text-align:left;">
        <div class="subtitle">Tertinggi</div>
        <div class="subname">{prev_max['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{prev_max['Prevalensi DBD per 100.000']:.2f}</div>
      </div>
      <div class="subcol-right" style="text-align:right;">
        <div class="subtitle">Terendah</div>
        <div class="subname">{prev_min['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{prev_min['Prevalensi DBD per 100.000']:.2f}</div>
      </div>
    </div>
  </div>

  <div class="metric-box">
    <div class="metric-title">Case Fatality Rate (CFR)</div>
    <div class="metric-value">{cfr_jabar:.2f}%</div>
    <div class="subrow">
      <div class="subcol-left" style="text-align:left;">
        <div class="subtitle">Tertinggi</div>
        <div class="subname">{cfr_max['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{cfr_max['CFR DBD (%)']:.2f}%</div>
      </div>
      <div class="subcol-right" style="text-align:right;">
        <div class="subtitle">Terendah</div>
        <div class="subname">{cfr_min['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{cfr_min['CFR DBD (%)']:.2f}%</div>
      </div>
    </div>
  </div>

  <div class="metric-box">
    <div class="metric-title">Prevalensi OR (Laki-laki vs Perempuan)</div>
    <div class="metric-value">{or_jabar:.2f}</div>
    <div class="subrow">
      <div class="subcol-left" style="text-align:left;">
        <div class="subtitle">Tertinggi</div>
        <div class="subname">{or_max['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{or_max['Prevalensi OR (Laki-laki vs Perempuan)']:.2f}</div>
      </div>
      <div class="subcol-right" style="text-align:right;">
        <div class="subtitle">Terendah</div>
        <div class="subname">{or_min['KABUPATEN/KOTA']}</div>
        <div class="subvalue">{or_min['Prevalensi OR (Laki-laki vs Perempuan)']:.2f}</div>
      </div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

final_df = df[["KABUPATEN/KOTA", "Prevalensi DBD per 100.000", "CFR DBD (%)", "Prevalensi OR (Laki-laki vs Perempuan)"]]

# ==== MAP

d = final_df.copy()
d['KABUPATEN/KOTA'] = d['KABUPATEN/KOTA'].astype(str).str.replace(' ', '', regex=False)
d['KABUPATEN/KOTA'] = d['KABUPATEN/KOTA'].apply(lambda x: x.lower())
gdf = gpd.read_file('gadm41_IDN_2.json')
gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())
merged = gdf.merge(d, left_on='NAME_2', right_on='KABUPATEN/KOTA')

fig, ax = plt.subplots(figsize=(20, 4))

list_info = ['Angka prevalensi DBD per 100.000 di setiap kota/kab dalam peta ini mengartikan bahwa dalam 100.000 penduduk terdapat banyaknya kasus dbd di kota/kab tersebut. Angka ini tidak bisa untuk perbandingan antar kota/kab',
'Angka dalam persen di CFR DBD di setiap kota/kab dalam peta ini mengartikan bahwa tinggi atau rendahnya resiko kematian karena dbd di kota/kab tersebut ditandai dengan tinggi atau rendahnya persentase CFR kota/kab tersebut. Semakin tinggi persenan CFR maka semakin tinggi resiko kematiannya.',
'Angka Prevalensi Odds Ratio di setiap kota/kab dalam peta ini menandakan bahwa laki - laki kemungkinan terkena DBD di kota/kab tersebut lebih tinggi atau lebih rendah dibandingkan perempuan. Angka ini tidak bisa digunakan untuk perbandingan antar kota/kab']

# col1, col2, col3 = st.columns([1, 1, 1])
for i, c in enumerate(st.columns([1, 1, 1])):
  with c:
    sub_data = d.drop(columns='KABUPATEN/KOTA').iloc[:, i]
    col = d.drop(columns='KABUPATEN/KOTA').columns[i]

    fig, ax = plt.subplots(figsize=(20, 4))

    with st.container(border=True):
        st.write(col)
        merged.plot(
            ax=ax,
            cmap='YlOrRd',
            legend=True,
            column=col,
            edgecolor='black'
        )
        ax.axis('off')
        st.pyplot(fig)
      
        with st.expander('Show Info'):
          st.write(list_info[i])


# ==============================
# TABEL COMPACT
# ==============================
st.markdown("<br><h5 style='text-align:center;'>Rekap Statistik per Kabupaten/Kota</h5>", unsafe_allow_html=True)
st.dataframe(final_df.style.format({
    "Prevalensi DBD per 100.000": "{:.2f}",
    "CFR DBD (%)": "{:.2f}",
    "Prevalensi OR (Laki-laki vs Perempuan)": "{:.2f}"
}))

row_index = st.selectbox("Pilih Data per Kota/Kab:", ['None'] + df['KABUPATEN/KOTA'].tolist())

def format_jumlah(x):
    return f"{x:.2f}"       

if row_index != 'None':
    with st.container(border=True):
        sub_df = df[df['KABUPATEN/KOTA'] == row_index]
        # st.write(f'## {row_index}')
        st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
          with st.container(border=True):
            st.write("##### Prevalensi DBD per 100.000")
            st.write(f'#### {format_jumlah(sub_df['Prevalensi DBD per 100.000'].values[0])}')
            # st.metric("Jumlah Penduduk Laki-Laki", format_jumlah(sub_df['Prevalensi DBD per 100.000'].values[0]))

        with col2:
          with st.container(border=True):
            st.write("##### CFR DBD (%)")
            st.write(f'#### {format_jumlah(sub_df['CFR DBD (%)'].values[0])}')
            # st.metric("Jumlah Kasus Laki-Laki", format_jumlah(sub_df['Jumlah Kasus Terkena DBD Laki Laki'].values[0]))

        with col3:
          with st.container(border=True):
            st.write("##### Prevalensi OR (Laki-laki vs Perempuan)")
            st.write(f'#### {format_jumlah(sub_df['Prevalensi OR (Laki-laki vs Perempuan)'].values[0])}')
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import json

# Konfigurasi halaman
st.set_page_config(layout='wide', page_title='Dashboard')

# Membaca data
data = pd.read_excel("epidem.xlsx", index_col=0)

def format_jumlah(x):
    return f"{x:,.0f}"  

# Custom CSS
st.markdown("""
<style>
    .risk-card {
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs([
    "DEMOGRAFI",
    "SEBARAN KASUS",
    "UKURAN EPIDEMOLOGI"])

total_penduduk_laki = sum(data["Jumlah Penduduk Laki Laki"])
total_penduduk_perempuan = sum(data["Jumlah Penduduk Perempuan"])
total_penduduk_pie = [total_penduduk_laki,total_penduduk_perempuan]
total_penduduk = total_penduduk_laki + total_penduduk_perempuan
piedf1 = pd.DataFrame({"Jenis Kelamin":["Laki-laki","Perempuan"],"Values":total_penduduk_pie})

def read_map():
    data = pd.read_excel("epidem.xlsx", index_col=0)
    data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].astype(str).str.replace(' ', '', regex=False)
    data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].apply(lambda x: x.lower())
    gdf = gpd.read_file('gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())
    merged = gdf.merge(data, left_on='NAME_2', right_on='KABUPATEN/KOTA')
    return merged

merged = read_map()
merged['Jumlah Kasus Terkena DBD Total'] = merged['Jumlah Kasus Terkena DBD Laki Laki'] + merged['Jumlah Kasus Terkena DBD Perempuan']
merged['Jumlah Kematian Karena DBD Total'] = merged['Jumlah Kematian Karena DBD Laki Laki'] + merged['Jumlah Kematian Karena DBD Perempuan']
merged['Jumlah Penduduk Total'] = merged['Jumlah Penduduk Laki Laki'] + merged['Jumlah Penduduk Perempuan']
# col1, col2, col3 = st.columns([1, 1, 1])

# with col1:
#     with st.container(border=True):
#         st.write("###### Jumlah Penduduk Total")
#         st.write(f'## {format_jumlah(total_penduduk)}')    

# with col2:
#     with st.container(border=True):
#         st.write("###### Jumlah Penduduk Laki-laki")
#         st.write(f'## {format_jumlah(total_penduduk_laki)}')

# with col3:
#     with st.container(border=True):
#         st.write("###### Jumlah Penduduk Perempuan")
#         st.write(f'## {format_jumlah(total_penduduk_perempuan)}')

# ====== CSS UNTUK BOX STATISTIK ======
with tab1:
    st.markdown("""
    <style>
    /* ====== GAYA UMUM ====== */

    /* Judul utama di atas */
    .demografi-title {
        text-align: center;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 25px;
        color: #000000 !important;
    }

    /* ===== BOX PUTIH DALAM COLUMN ===== */
    div[data-testid="stContainer"] > div:has(> div > div > div > div > div[data-testid="stMarkdownContainer"]) {
        border-radius: 12px;
        background-color: #ffffff !important;      /* FILL PUTIH SOLID */
        border: 1.5px solid rgba(100, 100, 100, 0.25) !important;
        padding: 25px 25px 30px 25px;
        text-align: center !important;
        box-shadow: 0 0 8px rgba(0,0,0,0.05);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    /* Hover efek */
    div[data-testid="stContainer"] > div:has(> div > div > div > div > div[data-testid="stMarkdownContainer"]):hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* ===== TEKS KECIL DI BOX ===== */
    div[data-testid="stMarkdownContainer"] h6 {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #FF6600 !important;
        margin-bottom: 8px !important;
        text-align: center !important;
    }

    /* ===== ANGKA UTAMA ===== */
    div[data-testid="stMarkdownContainer"] h2 {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #FF0000 !important;
        margin-top: 4px !important;
        text-align: center !important;
    }

    /* ===== MODE DARK ===== */
    @media (prefers-color-scheme: dark) {
        /* Box tetap fill putih solid */
        div[data-testid="stContainer"] > div:has(> div > div > div > div > div[data-testid="stMarkdownContainer"]) {
            background-color: #ffffff !important;
            border: 1.5px solid rgba(150,150,150,0.4) !important;
            color: #000000 !important;
        }

        /* Warna teks di dalam box */
        div[data-testid="stMarkdownContainer"] h6 {
            color: #FF6600 !important;
        }

        div[data-testid="stMarkdownContainer"] h2 {
            color: #FF0000 !important;
        }

        /* Judul utama tetap hitam di dark mode */
        .demografi-title {
            color: #000000 !important;
        }
    }
    </style>

    <h2 class="demografi-title">Demografi Jawa Barat Tahun 2024</h2>
    """, unsafe_allow_html=True)


    # ====== STRUKTUR LAYOUT ======
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.write("###### Jumlah Penduduk Total")
            st.write(f'## {format_jumlah(total_penduduk)}')    

    with col2:
        with st.container(border=True):
            st.write("###### Jumlah Penduduk Laki-laki")
            st.write(f'## {format_jumlah(total_penduduk_laki)}')

    with col3:
        with st.container(border=True):
            st.write("###### Jumlah Penduduk Perempuan")
            st.write(f'## {format_jumlah(total_penduduk_perempuan)}')

    merged_json = json.loads(merged.to_json())
    st.markdown("""
    <style>
    .equal-box {
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 15px;
        background-color: white;
        height: 620px;
    }
    </style>
    """, unsafe_allow_html=True)


    col4, col5 = st.columns([2, 1]) 

    with col4:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center;'>Peta Distribusi Penduduk</h3>", unsafe_allow_html=True)
            fig_map = px.choropleth(
                merged,
                geojson=merged_json,
                locations="NAME_2",
                featureidkey="properties.NAME_2",
                color="Jumlah Penduduk Total",
                hover_name="KABUPATEN/KOTA",  
                hover_data={
                    "Jumlah Penduduk Laki Laki": True,
                    "Jumlah Penduduk Perempuan": True,
                    "Jumlah Penduduk Total": True,
                    "NAME_2": False  
                },
                color_continuous_scale="YlOrRd",
                labels={"Jumlah Penduduk Total": "Jumlah Penduduk"}
            )

            fig_map.update_geos(
                fitbounds="locations",
                visible=False,
                projection_scale=9,
                center=dict(lat=-6.9, lon=107.6)
            )

            fig_map.update_layout(
                height=500,
                margin=dict(r=0, t=0, l=0, b=0),
                font=dict(
                    family="Arial",   
                    size=14,          
                    color="#333"      
                )
            )

            fig_map.update_traces(
                hovertemplate="<b>%{hovertext}</b><br>" +
                            "Laki-Laki: %{customdata[0]:,}<br>" +
                            "Perempuan: %{customdata[1]:,}<br>" +
                            "Total: %{z:,}<extra></extra>"
            )

            st.plotly_chart(
                fig_map, 
                use_container_width=True,
                config={"displayModeBar": True, "scrollZoom": False}
            )
            
    with col5:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center;'>Proporsi Penduduk</h3>", unsafe_allow_html=True)
            pie1 = px.pie(
                piedf1, values='Values', names="Jenis Kelamin",
                color='Jenis Kelamin',
                color_discrete_map={'Laki-laki': "#FFE066", 'Perempuan': "#FFA500"},
                hole=0.4
            )

            pie1.update_layout(height=500)
            st.plotly_chart(pie1, use_container_width=True)


    sub_df = data[['KABUPATEN/KOTA', 'Jumlah Penduduk Laki Laki', 'Jumlah Penduduk Perempuan']]
    sub_df['Jumlah Penduduk Total'] = data['Jumlah Penduduk Laki Laki'] + data['Jumlah Penduduk Perempuan']


    st.dataframe(sub_df)

    row_index = st.selectbox("Pilih Data per Kota/Kab:", ['Pilih Kota/Kabupaten'] + data['KABUPATEN/KOTA'].tolist())     

    if row_index != 'Pilih Kota/Kabupaten':
        with st.container(border=True):
            sub_df = data[data['KABUPATEN/KOTA'] == row_index]
            sub_df['total_penduduk'] = sub_df['Jumlah Penduduk Laki Laki'] + sub_df['Jumlah Penduduk Perempuan']
            # st.write(f'## {row_index}')
            st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
            st.divider()
            col1, col2= st.columns([1, 1])
            with col1:
                st.write("##### Jumlah Penduduk")
                st.write(f'## {format_jumlah(sub_df['total_penduduk'].values[0])}')
                st.write("##### Jumlah Penduduk Laki-Laki")
                st.write(f'## {format_jumlah(sub_df['Jumlah Penduduk Laki Laki'].values[0])}')
                st.write("##### Jumlah Penduduk Perempuan")
                st.write(f'## {format_jumlah(sub_df['Jumlah Penduduk Perempuan'].values[0])}')

            fig, ax = plt.subplots(figsize=(20, 4))
            provinsi = row_index.lower()
            provinsi = provinsi.replace(' ', '')
            a, b = data['Jumlah Kematian Karena DBD Laki Laki'].min(), data['Jumlah Kematian Karena DBD Laki Laki'].max()
            # col1, col2 = st.columns([1, 1])
            with col2:
                with st.container(border=True):
                    if provinsi:
                        if provinsi in merged['NAME_2'].values:
                            merged.plot(ax=ax, color='lightgray', edgecolor='black')
                            merged_selected = merged[merged['NAME_2'] == provinsi]
                            merged_selected.plot(
                                    ax=ax,
                                    cmap='YlOrRd',
                                    # legend=True,
                                    column="Jumlah Kematian Karena DBD Laki Laki",
                                    edgecolor='black',
                                    # vmin=a,
                                    # vmax=b
                                )
                        else:
                            st.write('#### Tidak ada map untuk Kab / Kota ini')
                    else:         
                        merged.plot(
                            ax=ax,
                            cmap='YlOrRd',
                            # legend=True,
                            column="Jumlah Kematian Karena DBD Laki Laki",
                            edgecolor='black',
                            # vmin=a,
                            # vmax=b
                        )
                    ax.axis('off')
                    st.pyplot(fig)

            # for col in list_col:
            #     fig, ax = plt.subplots(figsize=(20, 4))
            #     fig2, ax2 = plt.subplots(figsize=(20, 4))
            #     a, b = data[col + ' Laki Laki'].min(), data[col + ' Laki Laki'].max()
            #     col1, col2 = st.columns([1, 1])
            #     with col1:
            #         st.subheader(f'{col} Laki Laki')
            #         if provinsi:
            #             merged.plot(ax=ax, color='lightgray', edgecolor='black')
            #             merged_selected = merged[merged['NAME_2'] == provinsi]
            #             merged_selected.plot(
            #                     ax=ax,
            #                     cmap='YlOrRd',
            #                     legend=True,
            #                     column=col + " Laki Laki",
            #                     edgecolor='black',
            #                     vmin=a,
            #                     vmax=b
            #                 )
            #         else:
            #                 merged.plot(
            #                     ax=ax,
            #                     cmap='YlOrRd',
            #                     legend=True,
            #                     column=col + " Laki Laki",
            #                     edgecolor='black',
            #                     vmin=a,
            #                     vmax=b
            #                 )
            #         # ax.set_title('Laki Laki', fontsize=14)
            #         ax.axis('off')
            #         st.pyplot(fig)

            #     with col2:
            #         st.subheader(f'{col} Perempuan')
            #         if provinsi:
            #             merged.plot(ax=ax2, color='lightgray', edgecolor='black')
            #             merged_selected = merged[merged['NAME_2'] == provinsi]
            #             merged_selected.plot(
            #                     ax=ax2,
            #                     cmap='YlOrRd',
            #                     legend=True,
            #                     column=col + " Perempuan",
            #                     edgecolor='black',
            #                     vmin=a,
            #                     vmax=b
            #                 )
            #         else:
            #                 merged.plot(
            #                     ax=ax2,
            #                     cmap='YlOrRd',
            #                     legend=True,
            #                     column=col + " Perempuan",
            #                     edgecolor='black',
            #                     vmin=a,
            #                     vmax=b
            #                 )
            #         # ax2.set_title('Perempuan', fontsize=14)
            #         ax2.axis('off')
            #         st.pyplot(fig2)

# fig, ax = plt.subplots(figsize=(20, 4))
# fig2, ax2 = plt.subplots(figsize=(20, 4))
# fig3, ax3 = plt.subplots(figsize=(20, 4))
# list_col = ['Jumlah Kasus Terkena DBD', 'Jumlah Kematian Karena DBD']

# with st.container(border=True):
#     col = st.selectbox(
#         "",
#         options=list_col,
#         index=0,
#         label_visibility='collapsed',
#         placeholder='Pilih Kolom'
#     )
#     a, b = data[col + ' Laki Laki'].min(), data[col + ' Laki Laki'].max()
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col1:
#         # st.subheader('Laki Laki')
#         st.markdown(f"<h3 style='text-align:center;'>Laki Laki</h3>", unsafe_allow_html=True)
#         merged.plot(
#             ax=ax,
#             cmap='YlOrRd',
#             legend=True,
#             column=col + " Laki Laki",
#             edgecolor='black',
#             vmin=a,
#             vmax=b
#         )
#         ax.axis('off')
#         st.pyplot(fig)

#     with col2:
#         # st.subheader('Perempuan')
#         st.markdown(f"<h3 style='text-align:center;'>Perempuan</h3>", unsafe_allow_html=True)
#         merged.plot(
#             ax=ax2,
#             cmap='YlOrRd',
#             legend=True,
#             column=col + " Perempuan",
#             edgecolor='black',
#             vmin=a,
#             vmax=b
#         )
#         ax2.axis('off')
#         st.pyplot(fig2)

#     with col3:
#         # st.subheader('Total')
#         st.markdown(f"<h3 style='text-align:center;'>Total</h3>", unsafe_allow_html=True)
#         merged.plot(
#             ax=ax3,
#             cmap='YlOrRd',
#             legend=True,
#             column=col + " Total",
#             edgecolor='black',
#             vmin=a,
#             vmax=b
#         )
#         ax3.axis('off')
#         st.pyplot(fig3)
#     if col == 'Jumlah Kasus Terkena DBD':
#         with st.expander('Show Info'):
#             st.write("""
#             Jumlah kasus di setiap kota/kab dalam peta ini hanya menandakan jumlah kasus dari segi jumlahnya. Jumlah kasus ini tidak menandakan bahsa kasus terbanyak memiliki arti resiko terkena DBD tertinggi
#             """)
#     else:
#         with st.expander('Show Info'):
#             st.write("""
#             Jumlah kematian di setiap kota/kab dalam peta ini hanya menandakan jumlah kematian karena dbd dari dari segi jumlahnya. 
#             Jumlah kematian karena dbd ini tidak menandakan bahwa jumlah terbanyak memiliki arti resiko kematian tertinggi
#             """)

with tab2:
    total_kasus_laki = sum(data["Jumlah Kasus Terkena DBD Laki Laki"])
    total_kasus_perempuan = sum(data["Jumlah Kasus Terkena DBD Perempuan"])
    total_kasus_pie = [total_kasus_laki,total_kasus_perempuan]
    total_kasus = total_kasus_laki + total_kasus_perempuan
    piedf1 = pd.DataFrame({"Jenis Kelamin":["Laki-laki","Perempuan"],"Values":total_kasus_pie})

    total_kematian_laki = sum(data["Jumlah Kematian Karena DBD Laki Laki"])
    total_kematian_perempuan = sum(data["Jumlah Kematian Karena DBD Perempuan"])
    total_kematian_pie = [total_kematian_laki,total_kematian_perempuan]
    total_kematian = total_kematian_laki + total_kematian_perempuan
    piedf2 = pd.DataFrame({"Jenis Kelamin":["Laki-laki","Perempuan"],"Values":total_kematian_pie})

    def read_map():
        data = pd.read_excel("epidem.xlsx", index_col=0)
        data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].astype(str).str.replace(' ', '', regex=False)
        data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].apply(lambda x: x.lower())
        gdf = gpd.read_file('gadm41_IDN_2.json')
        gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
        gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())
        merged = gdf.merge(data, left_on='NAME_2', right_on='KABUPATEN/KOTA')
        return merged

    merged = read_map()
    merged['Jumlah Kasus Terkena DBD Total'] = merged['Jumlah Kasus Terkena DBD Laki Laki'] + merged['Jumlah Kasus Terkena DBD Perempuan']
    merged['Jumlah Kematian Karena DBD Total'] = merged['Jumlah Kematian Karena DBD Laki Laki'] + merged['Jumlah Kematian Karena DBD Perempuan']
    merged['Jumlah Penduduk Total'] = merged['Jumlah Penduduk Laki Laki'] + merged['Jumlah Penduduk Perempuan']

    # ==== tambahan untuk plotly ====
    merged["lon"] = merged.geometry.centroid.x
    merged["lat"] = merged.geometry.centroid.y
    merged_geojson = merged.__geo_interface__

    st.markdown(f"""
    <h2 style="text-align:center; font-weight:800; margin-top:10px; margin-bottom:25px;">
    Kasus DBD Jawa Barat Tahun 2024
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    st.markdown("""
    <style>
    /* ===== BOX UTAMA ===== */
    div[data-testid="stMarkdownContainer"] .stat-box {
        border-radius: 9px;
        background-color: #ffffff !important;      
        border: 1px solid rgba(120, 120, 120, 0.25) important;
        padding: 26px 30px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        color: #000 !important;              
        transition: transform 0.25s ease;
        box-shadow: none !important;                
    }

    /* Hover */
    div[data-testid="stMarkdownContainer"] .stat-box:hover {
        transform: translateY(-2px);
    }

    /* ===== TITLE DAN ANGKA ===== */
    div[data-testid="stMarkdownContainer"] .stat-title {
        font-size: 30px !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        color: #FF6600 !important;
    }

    div[data-testid="stMarkdownContainer"] .stat-total {
        font-size: 50px !important;
        font-weight: 850 !important;
        margin-bottom: 20px !important;
        color: #FF0000 !important;
    }

    /* ===== SUBROW ===== */
    div[data-testid="stMarkdownContainer"] .stat-subrow {
        display: flex !important;
        justify-content: space-between !important;
        width: 100%;
        margin-top: 10px !important;
    }

    div[data-testid="stMarkdownContainer"] .stat-subgroup-left { text-align: left !important; }
    div[data-testid="stMarkdownContainer"] .stat-subgroup-right { text-align: right !important; }

    div[data-testid="stMarkdownContainer"] .stat-subtitle {
        font-size: 20px !important;
        font-weight: 400 !important;
        margin-bottom: 4px !important;
        color: #FF6600 !important;
    }

    div[data-testid="stMarkdownContainer"] .stat-subvalue {
        font-size: 25px !important;
        font-weight: 800 !important;
        color: #FF0000 !important;
        line-height: 1.35;
    }

    /* ===== DARK MODE ===== */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMarkdownContainer"] .stat-box {
            background-color: #ffffff !important;     
            border: 1.8px solid rgba(180,180,180,0.45) !important; 
            box-shadow: none !important;
            color: #000 !important;                    
        }
    }
    </style>
    """, unsafe_allow_html=True)



    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-title">Total Kasus</div>
                <div class="stat-total">{format_jumlah(total_kasus)}</div>
                <div class="stat-subrow">
                    <div class="stat-subgroup-left">
                        <div class="stat-subtitle">Laki-laki</div>
                        <div class="stat-subvalue">{format_jumlah(total_kasus_laki)}</div>
                    </div>
                    <div class="stat-subgroup-right">
                        <div class="stat-subtitle">Perempuan</div>
                        <div class="stat-subvalue">{format_jumlah(total_kasus_perempuan)}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-title">Total Kematian</div>
                <div class="stat-total">{format_jumlah(total_kematian)}</div>
                <div class="stat-subrow">
                    <div class="stat-subgroup-left">
                        <div class="stat-subtitle">Laki-laki</div>
                        <div class="stat-subvalue">{format_jumlah(total_kematian_laki)}</div>
                    </div>
                    <div class="stat-subgroup-right">
                        <div class="stat-subtitle">Perempuan</div>
                        <div class="stat-subvalue">{format_jumlah(total_kematian_perempuan)}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    list_col = ['Jumlah Kasus Terkena DBD', 'Jumlah Kematian Karena DBD']

    with st.container(border=True):
        col = st.selectbox(
            "",
            options=list_col,
            index=0,
            label_visibility='collapsed',
            placeholder='Pilih Kolom'
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        # --- Laki Laki ---
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='text-align:center; font-weight:bold;'>Laki Laki</h3>", unsafe_allow_html=True)
                fig_map1 = px.choropleth(
                    merged,
                    geojson=merged_geojson,
                    locations=merged["KABUPATEN/KOTA"],  # gunakan nama daerah, bukan index
                    featureidkey="properties.KABUPATEN/KOTA",
                    color=col + " Laki Laki",
                    hover_name="KABUPATEN/KOTA",
                    hover_data={col + " Laki Laki": True, "KABUPATEN/KOTA": False},  # sembunyikan index
                    color_continuous_scale="YlOrRd",
                    range_color=(merged[col + " Laki Laki"].min(), merged[col + " Laki Laki"].max()),
                    scope="asia"
                )
                fig_map1.update_geos(fitbounds="locations", visible=False)
                fig_map1.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    dragmode=False,
                    coloraxis_showscale=True,
                    coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
                    font=dict(family="Arial"),
                    showlegend=False
                )
                st.plotly_chart(fig_map1, use_container_width=True, config={
                    'scrollZoom': False,
                    'displayModeBar': True,
                    'doubleClick': False,
                    'staticPlot': False
                })

        # --- Perempuan ---
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='text-align:center; font-weight:bold;'>Perempuan</h3>", unsafe_allow_html=True)
                fig_map2 = px.choropleth(
                    merged,
                    geojson=merged_geojson,
                    locations=merged["KABUPATEN/KOTA"],
                    featureidkey="properties.KABUPATEN/KOTA",
                    color=col + " Perempuan",
                    hover_name="KABUPATEN/KOTA",
                    hover_data={col + " Perempuan": True, "KABUPATEN/KOTA": False},
                    color_continuous_scale="YlOrRd",
                    range_color=(merged[col + " Perempuan"].min(), merged[col + " Perempuan"].max()),
                    scope="asia"
                )
                fig_map2.update_geos(fitbounds="locations", visible=False)
                fig_map2.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    dragmode=False,
                    coloraxis_showscale=True,
                    coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
                    font=dict(family="Arial"),
                    showlegend=False
                )
                st.plotly_chart(fig_map2, use_container_width=True, config={
                    'scrollZoom': False,
                    'displayModeBar': True,
                    'doubleClick': False,
                    'staticPlot': False
                })

        # --- Total ---
        with col3:
            with st.container(border=True):
                st.markdown("<h3 style='text-align:center; font-weight:bold;'>Total</h3>", unsafe_allow_html=True)
                fig_map3 = px.choropleth(
                    merged,
                    geojson=merged_geojson,
                    locations=merged["KABUPATEN/KOTA"],
                    featureidkey="properties.KABUPATEN/KOTA",
                    color=col + " Total",
                    hover_name="KABUPATEN/KOTA",
                    hover_data={col + " Total": True, "KABUPATEN/KOTA": False},
                    color_continuous_scale="YlOrRd",
                    range_color=(merged[col + " Total"].min(), merged[col + " Total"].max()),
                    scope="asia"
                )
                fig_map3.update_geos(fitbounds="locations", visible=False)
                fig_map3.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    dragmode=False,
                    coloraxis_showscale=True,
                    coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
                    font=dict(family="Arial"),
                    showlegend=False
                )
                st.plotly_chart(fig_map3, use_container_width=True, config={
                    'scrollZoom': False,
                    'displayModeBar': True,
                    'doubleClick': False,
                    'staticPlot': False
                })

        if col == 'Jumlah Kasus Terkena DBD':
            with st.expander('Show Info'):
                st.write("""
                Jumlah kasus hanya menandakan jumlah, bukan risiko tertinggi.
                """)
        else:
            with st.expander('Show Info'):
                st.write("""
                Jumlah kematian hanya menandakan jumlah kasus kematian, bukan risiko kematian tertinggi.
                """)

    pilihan = ["Jumlah Kasus DBD", "Jumlah Kematian Karena DBD"]
    row_index = col

    if row_index != 'Pilih Total Kasus atau Total Kematian':
        if row_index == "Jumlah Kasus Terkena DBD":
            with st.container(border=True):
                st.write("Jumlah Kasus DBD Jawa Barat 2024")
                st.bar_chart(data=data,y=['Jumlah Kasus Terkena DBD Laki Laki','Jumlah Kasus Terkena DBD Perempuan'],stack=False,color=["#FFE066","#FFA500"], y_label = 'Jumlah Kasus',x='KABUPATEN/KOTA')
            with st.container(border=True):
                st.write("Proporsi Kasus DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
                pie1 = px.pie(piedf1,values='Values', names="Jenis Kelamin",color='Jenis Kelamin', color_discrete_map={'Laki-laki': "#FFE066", 'Perempuan': "#FFA500"}, hole=0.4)
                st.plotly_chart(pie1)
                sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kasus Terkena DBD Laki Laki', 'Jumlah Kasus Terkena DBD Perempuan']]
                sub_df['Jumlah Kasus Terkeba DBD Total'] = data['Jumlah Kasus Terkena DBD Laki Laki'] + data['Jumlah Kasus Terkena DBD Perempuan']
        else:
            with st.container(border=True):
                st.write("Jumlah Kasus Kematian Akibat DBD Jawa Barat 2024")
                st.bar_chart(data=data,y=['Jumlah Kematian Karena DBD Laki Laki','Jumlah Kematian Karena DBD Perempuan'],stack=False,color=["#FFE066","#FFA500"], y_label = 'Jumlah Kematian',x='KABUPATEN/KOTA')
            with st.container(border=True):
                st.write("Proporsi Kematian Karena DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
                pie2 = px.pie(piedf2,values='Values', names="Jenis Kelamin",color='Jenis Kelamin', color_discrete_map={'Laki-laki': "#FFE066", 'Perempuan': "#FFA500"}, hole=0.4)
                st.plotly_chart(pie2)
                sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kematian Karena DBD Laki Laki', 'Jumlah Kematian Karena DBD Perempuan']]
                sub_df['Jumlah Kematian Karena DBD Total'] = data['Jumlah Kematian Karena DBD Laki Laki'] + data['Jumlah Kematian Karena DBD Perempuan']

    with st.expander('Tampilkan Data'):
        st.dataframe(sub_df)

    row_index = st.selectbox("Pilih Data per Kota/Kab:", ['Pilih Kota/Kab'] + data['KABUPATEN/KOTA'].tolist())     

    if row_index != 'Pilih Kota/Kab':
        with st.container(border=True):
            sub_df = data[data['KABUPATEN/KOTA'] == row_index]
            sub_df['total_kasus'] = sub_df['Jumlah Kasus Terkena DBD Laki Laki'] + sub_df['Jumlah Kasus Terkena DBD Perempuan']
            sub_df['total_kematian'] = sub_df['Jumlah Kematian Karena DBD Laki Laki'] + sub_df['Jumlah Kematian Karena DBD Perempuan']
            st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
            st.divider()
            col1, col2, col3= st.columns([1, 1, 1])

            with col1:
                st.write("##### Total Kasus")
                st.write(f'# {format_jumlah(sub_df["total_kasus"].values[0])}')
                st.write("##### Laki-laki")
                st.write(f'# {format_jumlah(sub_df["Jumlah Kasus Terkena DBD Laki Laki"].values[0])}')
                st.write("##### Perempuan")
                st.write(f'# {format_jumlah(sub_df["Jumlah Kasus Terkena DBD Perempuan"].values[0])}')

            with col2:
                st.write("##### Total Kematian")
                st.write(f'# {format_jumlah(sub_df["total_kematian"].values[0])}')
                st.write("##### Laki-laki")
                st.write(f'# {format_jumlah(sub_df["Jumlah Kematian Karena DBD Laki Laki"].values[0])}')
                st.write("##### Perempuan")
                st.write(f'# {format_jumlah(sub_df["Jumlah Kematian Karena DBD Perempuan"].values[0])}')

            fig, ax = plt.subplots(figsize=(20, 4))
            provinsi = row_index.lower()
            provinsi = provinsi.replace(' ', '')
            a, b = data['Jumlah Kematian Karena DBD Laki Laki'].min(), data['Jumlah Kematian Karena DBD Laki Laki'].max()
            # col1, col2 = st.columns([1, 1])
            with col3:
                with st.container(border=True):
                    if provinsi:
                        if provinsi in merged['NAME_2'].values:
                            merged.plot(ax=ax, color='lightgray', edgecolor='black')
                            merged_selected = merged[merged['NAME_2'] == provinsi]
                            merged_selected.plot(
                                    ax=ax,
                                    cmap='YlOrRd',
                                    # legend=True,
                                    column="Jumlah Kematian Karena DBD Laki Laki",
                                    edgecolor='black',
                                    # vmin=a,
                                    # vmax=b
                                )
                        else:
                            st.write('#### Tidak ada map untuk Kab / Kota ini')
                    else:
                        merged.plot(
                            ax=ax,
                            cmap='YlOrRd',
                            # legend=True,
                            column="Jumlah Kematian Karena DBD Laki Laki",
                            edgecolor='black',
                            # vmin=a,
                            # vmax=b
                        )

                    ax.axis('off')
                    st.pyplot(fig)

with tab3:
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
    Ukuran Statistik Epidemiologi DBD Jawa Barat Tahun 2024
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
    border-radius: 9px;
    background-color: rgba(255, 255, 255, 0.05);
    box-shadow: 0 6px 15px rgba(0,0,0,0.10);
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.25s ease;
    text-align: center;
    }}
    .metric-box:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
    }}

    /* ===== TEKS ===== */
    .metric-title {{
    font-size: 17px;
    font-weight: 700;
    color: #FF0000;
    margin-bottom: 6px;
    }}
    .metric-value {{
    font-size: 34px;
    font-weight: 1000;
    color: #FF0000;
    margin-bottom: 4px;
    }}
    .metric-sub {{
    color: #FF0000;
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
    color: #FF0000;
    margin-bottom: 2px;
    }}
    .subname {{
    font-size: 12px;
    font-weight: 400;
    color: #FF0000;
    }}
    .subvalue {{
    font-size: 13px;
    font-weight: 700;
    color: #FF0000;
    }}

    /* ===== DARK MODE OVERRIDE ===== */
    @media (prefers-color-scheme: dark) {{
    .metric-box {{
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        box-shadow: 0 6px 18px rgba(255,255,255,0.15) !important;
    }}
    .metric-title,
    .metric-value,
    .metric-sub,
    .subtitle,
    .subname,
    .subvalue {{
        color: #FF4500 !important;
    }}
    .metric-value {{
        color: #FF0000 !important;
    }}
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
            col = d.drop(columns='KABUPATEN/KOTA').columns[i]
            
            # Data untuk Plotly
            data_plot = merged.copy()
            data_plot["KABUPATEN/KOTA"] = data_plot["KABUPATEN/KOTA"].astype(str)

            merged_geojson = data_plot.__geo_interface__

            # Judul
            st.markdown(f"<h6 style='text-align:center; font-weight:bold;'>{col}</h6>", unsafe_allow_html=True)

            # Plot peta
            with st.container(border = True):
                fig_map3 = px.choropleth(
                    data_frame=data_plot,
                    geojson=merged_geojson,
                    locations="KABUPATEN/KOTA",
                    featureidkey="properties.NAME_2",
                    color=col,
                    hover_name="KABUPATEN/KOTA",
                    color_continuous_scale="YlOrRd",
                    range_color=(data_plot[col].min(), data_plot[col].max()),
                )
                fig_map3.update_geos(fitbounds="locations", visible=False)
                fig_map3.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
                    showlegend=True
                )

                st.plotly_chart(fig_map3, use_container_width=True, config={
                    'scrollZoom': False,
                    'displayModeBar': True
                })

                with st.expander('Show Info'):
                    st.write(list_info[i])



    # ==============================
    # TABEL COMPACT
    # ==============================
    st.markdown("<br><h5 style='text-align:center;'> Ukuran Statistik per Kabupaten/Kota</h5>", unsafe_allow_html=True)
    st.dataframe(final_df.style.format({
        "Prevalensi DBD per 100.000": "{:.2f}",
        "CFR DBD (%)": "{:.2f}",
        "Prevalensi OR (Laki-laki vs Perempuan)": "{:.2f}"
    }))

    row_index = st.selectbox("Pilih Data per Kota/Kab:", ['Pilih Wilayah'] + df['KABUPATEN/KOTA'].tolist())

    def format_jumlah(x):
        return f"{x:.2f}"       

    if row_index != 'Pilih Wilayah':
        with st.container(border=True):
            sub_df = df[df['KABUPATEN/KOTA'] == row_index]
            # st.write(f'## {row_index}')
            st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                with st.container(border=True):
                    st.write("###### Prevalensi DBD per 100.000")
                    st.write(f'## {format_jumlah(sub_df['Prevalensi DBD per 100.000'].values[0])}')
                # st.metric("Jumlah Penduduk Laki-Laki", format_jumlah(sub_df['Prevalensi DBD per 100.000'].values[0]))

            with col2:
                with st.container(border=True):
                    st.write("###### CFR DBD (%)")
                    st.write(f'## {format_jumlah(sub_df['CFR DBD (%)'].values[0])}')
                # st.metric("Jumlah Kasus Laki-Laki", format_jumlah(sub_df['Jumlah Kasus Terkena DBD Laki Laki'].values[0]))

            with col3:
                with st.container(border=True):
                    st.write("###### Prevalensi OR (Laki-laki vs Perempuan)")
                    st.write(f'## {format_jumlah(sub_df['Prevalensi OR (Laki-laki vs Perempuan)'].values[0])}')
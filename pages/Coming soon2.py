import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import plotly.express as px

# # Konfigurasi halaman
# st.set_page_config(layout='wide', page_title='Dashboard')
st.title("Coming Soon")
# # Membaca data
# data = pd.read_excel("epidem.xlsx", index_col=0)

# def format_jumlah(x):
#     return f"{x:,.0f}"  

# total_kasus_laki = sum(data["Jumlah Kasus Terkena DBD Laki Laki"])
# total_kasus_perempuan = sum(data["Jumlah Kasus Terkena DBD Perempuan"])
# total_kasus_pie = [total_kasus_laki,total_kasus_perempuan]
# total_kasus = total_kasus_laki + total_kasus_perempuan
# piedf1 = pd.DataFrame({"Jenis Kelamin":["Laki-laki","Perempuan"],"Values":total_kasus_pie})

# total_kematian_laki = sum(data["Jumlah Kematian Karena DBD Laki Laki"])
# total_kematian_perempuan = sum(data["Jumlah Kematian Karena DBD Perempuan"])
# total_kematian_pie = [total_kematian_laki,total_kematian_perempuan]
# total_kematian = total_kematian_laki + total_kematian_perempuan
# piedf2 = pd.DataFrame({"Jenis Kelamin":["Laki-laki","Perempuan"],"Values":total_kematian_pie})

# def read_map():
#     data = pd.read_excel("epidem.xlsx", index_col=0)
#     data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].astype(str).str.replace(' ', '', regex=False)
#     data['KABUPATEN/KOTA'] = data['KABUPATEN/KOTA'].apply(lambda x: x.lower())
#     gdf = gpd.read_file('gadm41_IDN_2.json')
#     gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
#     gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())
#     merged = gdf.merge(data, left_on='NAME_2', right_on='KABUPATEN/KOTA')
#     return merged

# merged = read_map()
# merged['Jumlah Kasus Terkena DBD Total'] = merged['Jumlah Kasus Terkena DBD Laki Laki'] + merged['Jumlah Kasus Terkena DBD Perempuan']
# merged['Jumlah Kematian Karena DBD Total'] = merged['Jumlah Kematian Karena DBD Laki Laki'] + merged['Jumlah Kematian Karena DBD Perempuan']
# merged['Jumlah Penduduk Total'] = merged['Jumlah Penduduk Laki Laki'] + merged['Jumlah Penduduk Perempuan']

# # ==== tambahan untuk plotly ====
# merged["lon"] = merged.geometry.centroid.x
# merged["lat"] = merged.geometry.centroid.y
# merged_geojson = merged.__geo_interface__

# st.markdown(f"""
# <h2 style="text-align:center; font-weight:800; margin-top:10px; margin-bottom:25px;">
# Kasus DBD Jawa Barat Tahun 2024
# </h2>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns([1, 1])

# st.markdown("""
# <style>
# /* ===== BOX UTAMA ===== */
# div[data-testid="stMarkdownContainer"] .stat-box {
#     border-radius: 9px;
#     background-color: #ffffff !important;      
#     border: 1px solid rgba(120, 120, 120, 0.25) important;
#     padding: 26px 30px;
#     display: flex;
#     flex-direction: column;
#     justify-content: space-between;
#     text-align: center;
#     color: #000 !important;              
#     transition: transform 0.25s ease;
#     box-shadow: none !important;                
# }

# /* Hover */
# div[data-testid="stMarkdownContainer"] .stat-box:hover {
#     transform: translateY(-2px);
# }

# /* ===== TITLE DAN ANGKA ===== */
# div[data-testid="stMarkdownContainer"] .stat-title {
#     font-size: 30px !important;
#     font-weight: 700 !important;
#     margin-bottom: 12px !important;
#     color: #FF6600 !important;
# }

# div[data-testid="stMarkdownContainer"] .stat-total {
#     font-size: 70px !important;
#     font-weight: 850 !important;
#     margin-bottom: 20px !important;
#     color: #FF0000 !important;
# }

# /* ===== SUBROW ===== */
# div[data-testid="stMarkdownContainer"] .stat-subrow {
#     display: flex !important;
#     justify-content: space-between !important;
#     width: 100%;
#     margin-top: 10px !important;
# }

# div[data-testid="stMarkdownContainer"] .stat-subgroup-left { text-align: left !important; }
# div[data-testid="stMarkdownContainer"] .stat-subgroup-right { text-align: right !important; }

# div[data-testid="stMarkdownContainer"] .stat-subtitle {
#     font-size: 20px !important;
#     font-weight: 400 !important;
#     margin-bottom: 4px !important;
#     color: #FF6600 !important;
# }

# div[data-testid="stMarkdownContainer"] .stat-subvalue {
#     font-size: 25px !important;
#     font-weight: 800 !important;
#     color: #FF0000 !important;
#     line-height: 1.35;
# }

# /* ===== DARK MODE ===== */
# @media (prefers-color-scheme: dark) {
#     div[data-testid="stMarkdownContainer"] .stat-box {
#         background-color: #ffffff !important;     
#         border: 1.8px solid rgba(180,180,180,0.45) !important; 
#         box-shadow: none !important;
#         color: #000 !important;                    
#     }
# }
# </style>
# """, unsafe_allow_html=True)



# with col1:
#     st.markdown(f"""
#         <div class="stat-box">
#             <div class="stat-title">Total Kasus</div>
#             <div class="stat-total">{format_jumlah(total_kasus)}</div>
#             <div class="stat-subrow">
#                 <div class="stat-subgroup-left">
#                     <div class="stat-subtitle">Laki-laki</div>
#                     <div class="stat-subvalue">{format_jumlah(total_kasus_laki)}</div>
#                 </div>
#                 <div class="stat-subgroup-right">
#                     <div class="stat-subtitle">Perempuan</div>
#                     <div class="stat-subvalue">{format_jumlah(total_kasus_perempuan)}</div>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""
#         <div class="stat-box">
#             <div class="stat-title">Total Kematian</div>
#             <div class="stat-total">{format_jumlah(total_kematian)}</div>
#             <div class="stat-subrow">
#                 <div class="stat-subgroup-left">
#                     <div class="stat-subtitle">Laki-laki</div>
#                     <div class="stat-subvalue">{format_jumlah(total_kematian_laki)}</div>
#                 </div>
#                 <div class="stat-subgroup-right">
#                     <div class="stat-subtitle">Perempuan</div>
#                     <div class="stat-subvalue">{format_jumlah(total_kematian_perempuan)}</div>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# list_col = ['Jumlah Kasus Terkena DBD', 'Jumlah Kematian Karena DBD']

# with st.container(border=True):
#     col = st.selectbox(
#         "",
#         options=list_col,
#         index=0,
#         label_visibility='collapsed',
#         placeholder='Pilih Kolom'
#     )

#     col1, col2, col3 = st.columns([1, 1, 1])
#     # --- Laki Laki ---
#     with col1:
#         with st.container(border=True):
#             st.markdown("<h3 style='text-align:center; font-weight:bold;'>Laki Laki</h3>", unsafe_allow_html=True)
#             fig_map1 = px.choropleth(
#                 merged,
#                 geojson=merged_geojson,
#                 locations=merged["KABUPATEN/KOTA"],  # gunakan nama daerah, bukan index
#                 featureidkey="properties.KABUPATEN/KOTA",
#                 color=col + " Laki Laki",
#                 hover_name="KABUPATEN/KOTA",
#                 hover_data={col + " Laki Laki": True, "KABUPATEN/KOTA": False},  # sembunyikan index
#                 color_continuous_scale="YlOrRd",
#                 range_color=(merged[col + " Laki Laki"].min(), merged[col + " Laki Laki"].max()),
#                 scope="asia"
#             )
#             fig_map1.update_geos(fitbounds="locations", visible=False)
#             fig_map1.update_layout(
#                 margin=dict(l=0, r=0, t=0, b=0),
#                 dragmode=False,
#                 coloraxis_showscale=True,
#                 coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
#                 font=dict(family="Arial"),
#                 showlegend=False
#             )
#             st.plotly_chart(fig_map1, use_container_width=True, config={
#                 'scrollZoom': False,
#                 'displayModeBar': True,
#                 'doubleClick': False,
#                 'staticPlot': False
#             })

#     # --- Perempuan ---
#     with col2:
#         with st.container(border=True):
#             st.markdown("<h3 style='text-align:center; font-weight:bold;'>Perempuan</h3>", unsafe_allow_html=True)
#             fig_map2 = px.choropleth(
#                 merged,
#                 geojson=merged_geojson,
#                 locations=merged["KABUPATEN/KOTA"],
#                 featureidkey="properties.KABUPATEN/KOTA",
#                 color=col + " Perempuan",
#                 hover_name="KABUPATEN/KOTA",
#                 hover_data={col + " Perempuan": True, "KABUPATEN/KOTA": False},
#                 color_continuous_scale="YlOrRd",
#                 range_color=(merged[col + " Perempuan"].min(), merged[col + " Perempuan"].max()),
#                 scope="asia"
#             )
#             fig_map2.update_geos(fitbounds="locations", visible=False)
#             fig_map2.update_layout(
#                 margin=dict(l=0, r=0, t=0, b=0),
#                 dragmode=False,
#                 coloraxis_showscale=True,
#                 coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
#                 font=dict(family="Arial"),
#                 showlegend=False
#             )
#             st.plotly_chart(fig_map2, use_container_width=True, config={
#                 'scrollZoom': False,
#                 'displayModeBar': True,
#                 'doubleClick': False,
#                 'staticPlot': False
#             })

#     # --- Total ---
#     with col3:
#         with st.container(border=True):
#             st.markdown("<h3 style='text-align:center; font-weight:bold;'>Total</h3>", unsafe_allow_html=True)
#             fig_map3 = px.choropleth(
#                 merged,
#                 geojson=merged_geojson,
#                 locations=merged["KABUPATEN/KOTA"],
#                 featureidkey="properties.KABUPATEN/KOTA",
#                 color=col + " Total",
#                 hover_name="KABUPATEN/KOTA",
#                 hover_data={col + " Total": True, "KABUPATEN/KOTA": False},
#                 color_continuous_scale="YlOrRd",
#                 range_color=(merged[col + " Total"].min(), merged[col + " Total"].max()),
#                 scope="asia"
#             )
#             fig_map3.update_geos(fitbounds="locations", visible=False)
#             fig_map3.update_layout(
#                 margin=dict(l=0, r=0, t=0, b=0),
#                 dragmode=False,
#                 coloraxis_showscale=True,
#                 coloraxis_colorbar=dict(title="", thickness=10, len=0.6),
#                 font=dict(family="Arial"),
#                 showlegend=False
#             )
#             st.plotly_chart(fig_map3, use_container_width=True, config={
#                 'scrollZoom': False,
#                 'displayModeBar': True,
#                 'doubleClick': False,
#                 'staticPlot': False
#             })

#     if col == 'Jumlah Kasus Terkena DBD':
#         with st.expander('Show Info'):
#             st.write("""
#             Jumlah kasus hanya menandakan jumlah, bukan risiko tertinggi.
#             """)
#     else:
#         with st.expander('Show Info'):
#             st.write("""
#             Jumlah kematian hanya menandakan jumlah kasus kematian, bukan risiko kematian tertinggi.
#             """)

# pilihan = ["Jumlah Kasus DBD", "Jumlah Kematian Karena DBD"]
# row_index = col

# if row_index != 'None':
#     if row_index == "Jumlah Kasus Terkena DBD":
#         with st.container(border=True):
#             st.write("Jumlah Kasus DBD Jawa Barat 2024")
#             st.bar_chart(data=data,y=['Jumlah Kasus Terkena DBD Laki Laki','Jumlah Kasus Terkena DBD Perempuan'],stack=False,color=["#FFE066","#FFA500"], y_label = 'Jumlah Kasus',x='KABUPATEN/KOTA')
#         with st.container(border=True):
#             st.write("Proporsi Kasus DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
#             pie1 = px.pie(piedf1,values='Values', names="Jenis Kelamin",color='Jenis Kelamin', color_discrete_map={'Laki-laki': "#FFE066", 'Perempuan': "#FFA500"}, hole=0.4)
#             st.plotly_chart(pie1)
#             sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kasus Terkena DBD Laki Laki', 'Jumlah Kasus Terkena DBD Perempuan']]
#             sub_df['Jumlah Kasus Terkeba DBD Total'] = data['Jumlah Kasus Terkena DBD Laki Laki'] + data['Jumlah Kasus Terkena DBD Perempuan']
#     else:
#         with st.container(border=True):
#             st.write("Jumlah Kasus Kematian Akibat DBD Jawa Barat 2024")
#             st.bar_chart(data=data,y=['Jumlah Kematian Karena DBD Laki Laki','Jumlah Kematian Karena DBD Perempuan'],stack=False,color=["#FFE066","#FFA500"], y_label = 'Jumlah Kematian',x='KABUPATEN/KOTA')
#         with st.container(border=True):
#             st.write("Proporsi Kematian Karena DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
#             pie2 = px.pie(piedf2,values='Values', names="Jenis Kelamin",color='Jenis Kelamin', color_discrete_map={'Laki-laki': "#FFE066", 'Perempuan': "#FFA500"}, hole=0.4)
#             st.plotly_chart(pie2)
#             sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kematian Karena DBD Laki Laki', 'Jumlah Kematian Karena DBD Perempuan']]
#             sub_df['Jumlah Kematian Karena DBD Total'] = data['Jumlah Kematian Karena DBD Laki Laki'] + data['Jumlah Kematian Karena DBD Perempuan']

# with st.expander('Tampilkan Data'):
#     st.dataframe(sub_df)

# row_index = st.selectbox("Pilih Data per Kota/Kab:", ['None'] + data['KABUPATEN/KOTA'].tolist())     

# if row_index != 'None':
#     with st.container(border=True):
#         sub_df = data[data['KABUPATEN/KOTA'] == row_index]
#         sub_df['total_kasus'] = sub_df['Jumlah Kasus Terkena DBD Laki Laki'] + sub_df['Jumlah Kasus Terkena DBD Perempuan']
#         sub_df['total_kematian'] = sub_df['Jumlah Kematian Karena DBD Laki Laki'] + sub_df['Jumlah Kematian Karena DBD Perempuan']
#         st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
#         st.divider()
#         col1, col2, col3= st.columns([1, 1, 1])

#         with col1:
#             st.write("##### Total Kasus")
#             st.write(f'# {format_jumlah(sub_df["total_kasus"].values[0])}')
#             st.write("##### Laki-laki")
#             st.write(f'# {format_jumlah(sub_df["Jumlah Kasus Terkena DBD Laki Laki"].values[0])}')
#             st.write("##### Perempuan")
#             st.write(f'# {format_jumlah(sub_df["Jumlah Kasus Terkena DBD Perempuan"].values[0])}')

#         with col2:
#             st.write("##### Total Kematian")
#             st.write(f'# {format_jumlah(sub_df["total_kematian"].values[0])}')
#             st.write("##### Laki-laki")
#             st.write(f'# {format_jumlah(sub_df["Jumlah Kematian Karena DBD Laki Laki"].values[0])}')
#             st.write("##### Perempuan")
#             st.write(f'# {format_jumlah(sub_df["Jumlah Kematian Karena DBD Perempuan"].values[0])}')

#         fig, ax = plt.subplots(figsize=(20, 4))
#         provinsi = row_index.lower()
#         provinsi = provinsi.replace(' ', '')
#         a, b = data['Jumlah Kematian Karena DBD Laki Laki'].min(), data['Jumlah Kematian Karena DBD Laki Laki'].max()
#         # col1, col2 = st.columns([1, 1])
#         with col3:
#             with st.container(border=True):
#                 if provinsi:
#                     if provinsi in merged['NAME_2'].values:
#                         merged.plot(ax=ax, color='lightgray', edgecolor='black')
#                         merged_selected = merged[merged['NAME_2'] == provinsi]
#                         merged_selected.plot(
#                                 ax=ax,
#                                 cmap='YlOrRd',
#                                 # legend=True,
#                                 column="Jumlah Kematian Karena DBD Laki Laki",
#                                 edgecolor='black',
#                                 # vmin=a,
#                                 # vmax=b
#                             )
#                     else:
#                         st.write('#### Tidak ada map untuk Kab / Kota ini')
#                 else:
#                     merged.plot(
#                         ax=ax,
#                         cmap='YlOrRd',
#                         # legend=True,
#                         column="Jumlah Kematian Karena DBD Laki Laki",
#                         edgecolor='black',
#                         # vmin=a,
#                         # vmax=b
#                     )

#                 ax.axis('off')
#                 st.pyplot(fig)
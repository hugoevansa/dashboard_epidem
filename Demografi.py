import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(layout='wide', page_title='Dashboard')

# Membaca data
data = pd.read_excel("epidem.xlsx", index_col=0)

def format_jumlah(x):
    return f"{x:,.0f}"  

total_penduduk_laki = sum(data["Jumlah Penduduk Laki Laki"])
total_penduduk_perempuan = sum(data["Jumlah Penduduk Perempuan"])
total_penduduk_pie = [total_penduduk_laki,total_penduduk_perempuan]
total_penduduk = total_penduduk_laki + total_penduduk_perempuan
piedf1 = pd.DataFrame({"Jenis Kelamin":["Laki","Perempuan"],"Values":total_penduduk_pie})

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

st.markdown("""
<style>
h1 {
    font-size: 32px !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)
st.title("Demografi Jawa Barat")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    with st.container(border=True):
        st.write("### Jumlah Penduduk Laki Laki")
        st.write(f'#### {format_jumlah(total_penduduk_laki)}')

with col2:
    with st.container(border=True):
        st.write("### Jumlah Penduduk Perempuan")
        st.write(f'#### {format_jumlah(total_penduduk_perempuan)}')

with col3:
    with st.container(border=True):
        st.write("### Jumlah Penduduk Total")
        st.write(f'#### {format_jumlah(total_penduduk)}')

fig4, ax4 = plt.subplots(figsize=(20,4))
with st.container(border=True):
    col4, col5 = st.columns([1, 1])  
    with col4:
        st.markdown(f"<h3 style='text-align:center;'>Jumlah Penduduk Total</h3>",unsafe_allow_html=True)
        merged.plot(
            ax=ax4,
            cmap='YlOrRd',
            legend=True,
            column="Jumlah Penduduk Total",
            edgecolor='black',

        )
        ax4.axis('off')
        st.pyplot(fig4)

    with col5:
        st.markdown(f"<h3 style='text-align:center;'>Proporsi Penduduk</h3>",unsafe_allow_html=True)
        pie1 = px.pie(
            piedf1,
            values='Values',
            names="Jenis Kelamin",
            color='Jenis Kelamin',
            color_discrete_map={'Laki': "#62aec5", 'Perempuan': "#e64072"},
            hole=0.4
        )
        st.plotly_chart(pie1, use_container_width=True)

sub_df = data[['KABUPATEN/KOTA', 'Jumlah Penduduk Laki Laki', 'Jumlah Penduduk Perempuan']]
sub_df['Jumlah Penduduk Total'] = data['Jumlah Penduduk Laki Laki'] + data['Jumlah Penduduk Perempuan']


st.dataframe(sub_df)

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

row_index = st.selectbox("Pilih Data per Kota/Kab:", ['None'] + data['KABUPATEN/KOTA'].tolist())     

if row_index != 'None':
    with st.container(border=True):
        sub_df = data[data['KABUPATEN/KOTA'] == row_index]
        sub_df['total_penduduk'] = sub_df['Jumlah Penduduk Laki Laki'] + sub_df['Jumlah Penduduk Perempuan']
        # st.write(f'## {row_index}')
        st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
        st.divider()
        col1, col2= st.columns([1, 1])
        with col1:
            st.write("# Jumlah Penduduk")
            st.write(f'### {format_jumlah(sub_df['total_penduduk'].values[0])}')
            st.write("# Jumlah Penduduk Laki-Laki")
            st.write(f'### {format_jumlah(sub_df['Jumlah Penduduk Laki Laki'].values[0])}')
            st.write("# Jumlah Penduduk Perempuan")
            st.write(f'### {format_jumlah(sub_df['Jumlah Penduduk Perempuan'].values[0])}')

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

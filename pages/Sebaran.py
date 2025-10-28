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

total_kasus_laki = sum(data["Jumlah Kasus Terkena DBD Laki Laki"])
total_kasus_perempuan = sum(data["Jumlah Kasus Terkena DBD Perempuan"])
total_kasus_pie = [total_kasus_laki,total_kasus_perempuan]
total_kasus = total_kasus_laki + total_kasus_perempuan
piedf1 = pd.DataFrame({"Jenis Kelamin":["Laki","Perempuan"],"Values":total_kasus_pie})

total_kematian_laki = sum(data["Jumlah Kematian Karena DBD Laki Laki"])
total_kematian_perempuan = sum(data["Jumlah Kematian Karena DBD Perempuan"])
total_kematian_pie = [total_kematian_laki,total_kematian_perempuan]
total_kematian = total_kematian_laki + total_kematian_perempuan
piedf2 = pd.DataFrame({"Jenis Kelamin":["Laki","Perempuan"],"Values":total_kematian_pie})

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

st.title("Kasus DBD Jawa Barat 2024")

_, col1, _, col2, _ = st.columns([0.9, 1.4, 0.2, 1.4, 0.9])

with col1:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align:center;">
                <h4>Jumlah Kasus</h4>
                <h3>{format_jumlah(total_kasus)}</h3>
                <h4>Laki - Laki</h4>
                <h3>{format_jumlah(total_kasus_laki)}</h3>
                <h4>Perempuan</h4>
                <h3>{format_jumlah(total_kasus_perempuan)}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align:center;">
                <h4>Jumlah Kematian</h4>
                <h3>{format_jumlah(total_kematian)}</h3>
                <h4>Laki - Laki</h4>
                <h3>{format_jumlah(total_kematian_laki)}</h3>
                <h4>Perempuan</h4>
                <h3>{format_jumlah(total_kematian_perempuan)}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )


fig, ax = plt.subplots(figsize=(20, 4))
fig2, ax2 = plt.subplots(figsize=(20, 4))
fig3, ax3 = plt.subplots(figsize=(20, 4))
list_col = ['Jumlah Kasus Terkena DBD', 'Jumlah Kematian Karena DBD']

with st.container(border=True):
    col = st.selectbox(
        "",
        options=list_col,
        index=0,
        label_visibility='collapsed',
        placeholder='Pilih Kolom'
    )
    a, b = data[col + ' Laki Laki'].min(), data[col + ' Laki Laki'].max()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        # st.subheader('Laki Laki')
        st.markdown(f"<h3 style='text-align:center;'>Laki Laki</h3>", unsafe_allow_html=True)
        merged.plot(
            ax=ax,
            cmap='YlOrRd',
            legend=True,
            column=col + " Laki Laki",
            edgecolor='black',
            vmin=a,
            vmax=b
        )
        ax.axis('off')
        st.pyplot(fig)

    with col2:
        # st.subheader('Perempuan')
        st.markdown(f"<h3 style='text-align:center;'>Perempuan</h3>", unsafe_allow_html=True)
        merged.plot(
            ax=ax2,
            cmap='YlOrRd',
            legend=True,
            column=col + " Perempuan",
            edgecolor='black',
            vmin=a,
            vmax=b
        )
        ax2.axis('off')
        st.pyplot(fig2)

    with col3:
        # st.subheader('Total')
        st.markdown(f"<h3 style='text-align:center;'>Total</h3>", unsafe_allow_html=True)
        merged.plot(
            ax=ax3,
            cmap='YlOrRd',
            legend=True,
            column=col + " Total",
            edgecolor='black',
            vmin=a,
            vmax=b
        )
        ax3.axis('off')
        st.pyplot(fig3)
    if col == 'Jumlah Kasus Terkena DBD':
        with st.expander('Show Info'):
            st.write("""
            Jumlah kasus di setiap kota/kab dalam peta ini hanya menandakan jumlah kasus dari segi jumlahnya. Jumlah kasus ini tidak menandakan bahsa kasus terbanyak memiliki arti resiko terkena DBD tertinggi
            """)
    else:
        with st.expander('Show Info'):
            st.write("""
            Jumlah kematian di setiap kota/kab dalam peta ini hanya menandakan jumlah kematian karena dbd dari dari segi jumlahnya. 
            Jumlah kematian karena dbd ini tidak menandakan bahwa jumlah terbanyak memiliki arti resiko kematian tertinggi
            """)

# Pilih baris
    pilihan = ["Jumlah Kasus DBD", "Jumlah Kematian Karena DBD"]
    # row_index = st.selectbox("Pilih Chart yang diinginkan", pilihan)
    row_index = col

    if row_index != 'None':
        if row_index == "Jumlah Kasus Terkena DBD":
            # with st.container(border=True):
                st.write("Jumlah Kasus DBD Jawa Barat 2024")
                st.bar_chart(data=data,y=['Jumlah Kasus Terkena DBD Laki Laki','Jumlah Kasus Terkena DBD Perempuan'],stack=False,color=["#62aec5","#e64072"], y_label = 'Jumlah Kasus',x='KABUPATEN/KOTA')
                st.write("Proporsi Kasus DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
                pie1 = px.pie(piedf1,values='Values', names="Jenis Kelamin",color='Jenis Kelamin',
                    color_discrete_map={'Laki': "#62aec5", 'Perempuan': "#e64072"}, hole=0.4)
                st.plotly_chart(pie1)
                sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kasus Terkena DBD Laki Laki', 'Jumlah Kasus Terkena DBD Perempuan']]
                sub_df['Jumlah Kasus Terkeba DBD Total'] = data['Jumlah Kasus Terkena DBD Laki Laki'] + data['Jumlah Kasus Terkena DBD Perempuan']
        else:
            # with st.container(border=True):
                st.write("Jumlah Kasus Kematian Akibat DBD Jawa Barat 2024")
                st.bar_chart(data=data,y=['Jumlah Kematian Karena DBD Laki Laki','Jumlah Kematian Karena DBD Perempuan'],stack=False,color=["#62aec5","#e64072"], y_label = 'Jumlah Kematian',x='KABUPATEN/KOTA')

                st.write("Proporsi Kematian Karena DBD Jawa Barat 2024 Berdasarkan Jenis Kelamin")
                pie2 = px.pie(piedf2,values='Values', names="Jenis Kelamin",color='Jenis Kelamin',
                    color_discrete_map={'Laki': "#62aec5", 'Perempuan': "#e64072"}, hole=0.4)
                st.plotly_chart(pie2)
                sub_df = data[['KABUPATEN/KOTA', 'Jumlah Kematian Karena DBD Laki Laki', 'Jumlah Kematian Karena DBD Perempuan']]
                sub_df['Jumlah Kematian Karena DBD Total'] = data['Jumlah Kematian Karena DBD Laki Laki'] + data['Jumlah Kematian Karena DBD Perempuan']

with st.expander('Show DF'):
    st.dataframe(sub_df)

row_index = st.selectbox("Pilih Data per Kota/Kab:", ['None'] + data['KABUPATEN/KOTA'].tolist())     

if row_index != 'None':
    with st.container(border=True):
        sub_df = data[data['KABUPATEN/KOTA'] == row_index]
        sub_df['total_kasus'] = sub_df['Jumlah Kasus Terkena DBD Laki Laki'] + sub_df['Jumlah Kasus Terkena DBD Perempuan']
        sub_df['total_kematian'] = sub_df['Jumlah Kematian Karena DBD Laki Laki'] + sub_df['Jumlah Kematian Karena DBD Perempuan']
        # st.write(f'## {row_index}')
        st.markdown(f"<h1 style='text-align:center;'>{row_index}</h1>", unsafe_allow_html=True)
        st.divider()
        col1, col2, col3= st.columns([1, 1, 1])
        with col1:
            st.write("#### Total")
            st.write(f'#### {format_jumlah(sub_df['total_kasus'].values[0])}')
            st.write("#### Laki-Laki")
            st.write(f'#### {format_jumlah(sub_df['Jumlah Kasus Terkena DBD Laki Laki'].values[0])}')
            st.write("#### Perempuan")
            st.write(f'#### {format_jumlah(sub_df['Jumlah Kasus Terkena DBD Perempuan'].values[0])}')

        with col2:
            st.write("#### Total")
            st.write(f'#### {format_jumlah(sub_df['total_kematian'].values[0])}')
            st.write("#### Laki-Laki")
            st.write(f'#### {format_jumlah(sub_df['Jumlah Kematian Karena DBD Laki Laki'].values[0])}')
            st.write("#### Perempuan")
            st.write(f'#### {format_jumlah(sub_df['Jumlah Kematian Karena DBD Perempuan'].values[0])}')

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
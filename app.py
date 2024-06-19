import pymysql
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

# Membuat koneksi ke database MySQL
conn = pymysql.connect(
    host="kubela.id",
    port=3306,
    user="davis2024irwan",
    password="wh451n9m@ch1n3",
    database="aw"
)

# Cek koneksi berhasil
if conn:
    print('Connected to MySQL database')

# Query SQL untuk mengambil data penjualan per tahun
query = """
    SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
    FROM dimtime
    JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
    GROUP BY CalendarYear
    ORDER BY CalendarYear
"""

# Menjalankan query dan membuat DataFrame dari hasilnya
df_sales = pd.read_sql(query, conn)

# Konversi kolom 'Year' ke tipe data integer
df_sales['Year'] = df_sales['Year'].astype(int)

# Menampilkan judul dashboard
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# Menampilkan DataFrame di Streamlit dalam bentuk tabel
st.subheader('1. Data Penjualan Tahunan')
st.dataframe(df_sales)

# Rentang tahun yang tersedia
tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

# Pilihan untuk memilih rentang tahun menggunakan slider
year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

# Filter data berdasarkan rentang tahun yang dipilih
df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

# Plot perbandingan total penjualan per tahun dengan Matplotlib
plt.figure(figsize=(12, 6))
plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
plt.xlabel('Tahun', fontsize=14)
plt.ylabel('Total Penjualan', fontsize=14)
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan </h2>", unsafe_allow_html=True)
st.pyplot(plt)

# Query data untuk bubble plot
query = '''
SELECT 
  st.SalesTerritoryRegion AS Country,
  SUM(fs.SalesAmount) AS TotalSales  
FROM factinternetsales fs
JOIN dimsalesterritory st
  ON fs.SalesTerritoryKey = st.SalesTerritoryKey
GROUP BY Country
'''

# Membuat DataFrame dari hasil query
df_bubble = pd.read_sql(query, conn)

# Tambahkan argumen s untuk ukuran bubble
plt.figure(figsize=(14, 12))
plt.scatter(x=df_bubble['Country'], 
            y=df_bubble['TotalSales'],
            s=df_bubble['TotalSales'] / 1000,  # Ukuran bubble diatur lebih kecil untuk visibilitas yang lebih baik
            c='b',
            alpha=0.6,  # Menambahkan transparansi untuk visibilitas yang lebih baik
            edgecolors='w',  # Menambahkan border putih pada bubble
            linewidth=0.5)

# Menambahkan label untuk sumbu x dan y serta judul plot
plt.xlabel('Country')
plt.ylabel('Total Sales')  
plt.title('Bubble Plot Hubungan Wilayah dan Penjualan')

# Menambahkan grid untuk memudahkan pembacaan plot
plt.grid(True)

# Menampilkan plot di Streamlit
st.markdown("<h2 style='text-align: center;'>2. Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
st.pyplot(plt)

# Query data untuk pie chart
query = '''
SELECT
    st.SalesTerritoryRegion,
    SUM(fs.SalesAmount) AS TotalSales
FROM
    factinternetsales fs
JOIN
    dimsalesterritory st ON fs.SalesTerritoryKey = st.SalesTerritoryKey
GROUP BY
    st.SalesTerritoryRegion
'''

# Jalankan query dan simpan hasilnya ke dalam DataFrame
df_sales_by_region = pd.read_sql(query, conn)

# Buat visualisasi proporsi penjualan per wilayah atau region
plt.figure(figsize=(10, 6))
plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
plt.title('Proporsi Penjualan per Wilayah atau Region')
plt.axis('equal')  # Membuat pie chart menjadi lingkaran

# Menampilkan plot di Streamlit
st.markdown("<h2 style='text-align: center;'>3. Proporsi Penjualan per Wilayah atau Region</h2>", unsafe_allow_html=True)
st.pyplot(plt)

# Query data untuk bar plot
query = '''
SELECT
    pc.EnglishProductCategoryName AS ProductCategory,
    SUM(fs.SalesAmount) AS TotalSales
FROM
    factinternetsales fs
JOIN
    dimproduct p ON fs.ProductKey = p.ProductKey
JOIN
    dimproductsubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey
JOIN
    dimproductcategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
GROUP BY
    pc.EnglishProductCategoryName
'''

# Baca ke DataFrame
df = pd.read_sql(query, conn)

# Menutup koneksi setelah selesai digunakan
conn.close()

# Buat figure dan axes
fig, ax = plt.subplots(figsize=(10, 6))

# Plot bar (lebih cocok daripada histogram untuk kategori)
ax.bar(df['ProductCategory'], df['TotalSales'], color='blue')

# Setting label        
ax.set(title='Komposisi Penjualan per Kategori Produk',
       ylabel='Total Penjualan',   
       xlabel='Kategori Produk')

# Rotasi label x untuk lebih baik
plt.xticks(rotation=45)

# Menampilkan plot di Streamlit
st.markdown("<h2 style='text-align: center;'>4. Komposisi Penjualan per Kategori Produk</h2>", unsafe_allow_html=True)
st.pyplot(fig)

import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat data Adventure Works
def load_adventure_works_data():
    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )

    # Query SQL untuk mengambil data penjualan per tahun
    query_sales = """
        SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
        FROM dimtime
        JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
        GROUP BY CalendarYear
        ORDER BY CalendarYear
    """
    df_sales = pd.read_sql(query_sales, conn)

    # Ensure Year column is of integer type
    df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
    
    conn.close()
    return df_sales

# Fungsi untuk memuat data IMDB
def load_imdb_data():
    fn1 = 'imdb.csv'
    return pd.read_csv(fn1, encoding='latin1')

# Load Adventure Works data
df_sales = load_adventure_works_data()

# Menampilkan judul di halaman web
st.title("Final Project Mata Kuliah Data Visualisasi")

# Menambahkan sidebar
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.title("Scraping Website IMDB")
    st.write(df_imdb)

    # Visualisasi Bar Chart Rating untuk Setiap Judul Film
    st.subheader('Bar Chart Rating untuk Setiap Judul Film')

    # Grupkan data berdasarkan judul film dan rating
    grouped_df = df_imdb.groupby('Rate')['Judul'].first().reset_index()

    # Plot bar chart dengan sumbu judul di y dan rating di x
    plt.figure(figsize=(12, 8))
    plt.barh(grouped_df['Judul'], grouped_df['Rate'], color='skyblue')  # Menggunakan plt.barh untuk horizontal bar chart
    plt.xlabel('Rating')
    plt.ylabel('Judul Film')
    plt.title('Bar Chart Rating untuk Setiap Judul Film')
    plt.grid(True)
    st.pyplot(plt)

else:
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('1. Data Penjualan Tahunan')
    st.dataframe(df_sales)

    # Check if the DataFrame is not empty
    if not df_sales.empty:
        try:
            # Ensure Year column is of integer type
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
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
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

    # Query data untuk bubble plot
    query_bubble = '''
    SELECT 
      st.SalesTerritoryRegion AS Country,
      SUM(fs.SalesAmount) AS TotalSales  
    FROM factinternetsales fs
    JOIN dimsalesterritory st
      ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY Country
    '''

    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )

    df_bubble = pd.read_sql(query_bubble, conn)

      # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('2. Hubungan Penjualan berdasarkan region')
    st.dataframe(df_bubble)

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
    st.markdown("<h2 style='text-align: center;'>Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    # Query data untuk pie chart
    query_pie = '''
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

    df_sales_by_region = pd.read_sql(query_pie, conn)

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('3. Proporsi Penjualan Berdasarkan Wilayah atau Region')
    st.dataframe(df_sales_by_region)

    # Buat visualisasi proporsi penjualan per wilayah atau region
    plt.figure(figsize=(10, 6))
    plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
    plt.title('Proporsi Penjualan per Wilayah atau Region')
    plt.axis('equal')  # Membuat pie chart menjadi lingkaran

    # Menampilkan plot di Streamlit
    st.markdown("<h2 style='text-align: center;'>Proporsi Penjualan per Wilayah atau Region</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    # Query data untuk bar plot
    query_bar = '''
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

    df_bar = pd.read_sql(query_bar, conn)

    # Menampilkan DataFrame di Streamlit dalam bentuk tabel
    st.subheader('4. Komposisi Penjualan Berdasarkan Kategori Produk')
    st.dataframe(df_bar)

    # Menutup koneksi setelah selesai digunakan
    conn.close()

    # Buat figure dan axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bar (lebih cocok daripada histogram untuk kategori)
    ax.bar(df_bar['ProductCategory'], df_bar['TotalSales'], color='blue')

    # Setting label        
    ax.set(title='Komposisi Penjualan per Kategori Produk',
           ylabel='Total Penjualan',   
           xlabel='Kategori Produk')

    # Rotasi label x untuk lebih baik
    plt.xticks(rotation=45)

    # Menampilkan plot di Streamlit
    st.markdown("<h2 style='text-align: center;'>Komposisi Penjualan per Kategori Produk</h2>", unsafe_allow_html=True)
    st.pyplot(fig)

import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat Adventure Works data
def load_adventure_works_data():
    conn = pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

    # SQL query untuk mengambil yearly sales data
    query_sales = """
        SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
        FROM dimtime
        JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
        GROUP BY CalendarYear
        ORDER BY CalendarYear
    """
    df_sales = pd.read_sql(query_sales, conn)
    
    # Memastikan kolom year adalah integer
    df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
    
    conn.close()
    return df_sales

# Fungsi memuat IMDB data
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1').head(10)  # Using only the first 10 rows

# Streamlit title
st.markdown("""
    <style>
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #4b4b4b;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #fc466b, #3f5efb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <h1 class="title">Final Project Mata Kuliah Data Visualisasi</h1>
    """, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1, h2 {
        color: #4b4b4b;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .css-1aumxhk {
        color: #4b4b4b;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar option untuk memilih data di display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Handling IMDB Top Movies data
if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.write("<h1 style='text-align: center; color: black;'>Scraping Website IMDB</h1>", unsafe_allow_html=True)
    st.write(df_imdb)

    # Check keberadaan kolom
    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # kolom yang diharapkan
    if set(expected_columns).issubset(df_imdb.columns):
        # 1. Comparison : Number of Movies per Year
        year_counts = df_imdb['tahun'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.index.astype(str), year_counts.values, color='skyblue')
        plt.title('Perbandingan Jumlah Film per Tahun')
        plt.xlabel('Tahun')
        plt.ylabel('Jumlah Film')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

        st.markdown(""" <p style='color: black;'>
        Dari visualisasi tersebut dapat di analisis bahwa jumlah film dapat berubah tiap tahunnya, 
        seperti pada tahun 1994 film baru mencapai 2 film. Berbeda dengan tahun sebelumnya yang hanya ada 1 film.</p> 
        """,unsafe_allow_html=True)
        
        # 2. Relationship : Scatter Plot of Film Duration vs Rate
        plt.figure(figsize=(10, 6))
        plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
        plt.title('Hubungan Antara Durasi Film dan Rate')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Rate')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown(""" <p style='color: black;'>
         Dari visualisasi tersebut dapat di analisis bahwa terdapat hubungan antara durasi film dan rating 
         yang digambarkan dengan terbentuknya pola tren.</p>  
        """,unsafe_allow_html=True)
            
        # 3. Distribution : Histogram of Film Duration Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df_imdb['durasi'], bins=20, color='green', edgecolor='black')
        plt.title('Distribusi Durasi Film')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Frekuensi')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown(""" <p style='color: black;'>
        Dari visualisasi tersebut menggambarkan distribusi durasi film yang ada, 
        dari visualisasi tersebut dapat disimpulkan frekuensi dari masing-masing durasi film yang ada adalah sama, yakni memiliki 1 frekuensi.</p>
        """,unsafe_allow_html=True)
        
        # 4. Composition : Pie Chart of Movie Count per Age Rating
        age_counts = df_imdb['age'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Komposisi Film Berdasarkan Age Rating')
        plt.axis('equal')
        st.pyplot(plt)

        st.markdown(""" <p style='color: black;'>
        Dari visualisasi tersebut dapat di analisis bahwa film-film ditonton dari berbagai kalangan usia, 
        pada pie chart tersebut dapat disimpulkan kalangan yang menonton film rata-rata adalah usia remaja.</p> 
        """,unsafe_allow_html=True)

    else:
        st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")

# Handling Adventure Works data
else:
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Memuat Adventure Works data
    df_sales = load_adventure_works_data()

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.markdown("<p style='color: black; font-size: 18px;'>1. Data Penjualan Tahunan</p>", unsafe_allow_html=True)
    st.dataframe(df_sales)

    # cek DataFrame memastikan tidak kosong 
    if not df_sales.empty:
        try:
            # Memastikan kolom Year merupakan integer
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            # Pilihan untuk select year range menggunakan slider
            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            # Filter data berdasarkan year range
            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            # Plot comparison of total sales per year using Matplotlib
            plt.figure(figsize=(12, 6))
            plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
            plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
            plt.xlabel('Tahun', fontsize=14)
            plt.ylabel('Total Penjualan', fontsize=14)
            plt.grid(True)

            # Display plot in Streamlit
            st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan </h2>", unsafe_allow_html=True)
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
            Dari visualisasi di atas dapat dilihat adanya kenaikan penjualan tertinggi di tahun 2003 dan penjualan yang menurun di tahun 2004.</p>
            """,unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

    # Query data bubble plot
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
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

    df_bubble = pd.read_sql(query_bubble, conn)

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.markdown("<p style='color: black; font-size: 18px;'>2. Hubungan Penjualan berdasarkan region</p>", unsafe_allow_html=True)
    st.dataframe(df_bubble)

    # Adjust bubble size for better visibility
    plt.figure(figsize=(14, 12))
    plt.scatter(x=df_bubble['Country'], 
                y=df_bubble['TotalSales'],
                s=df_bubble['TotalSales'] / 1000,  # Adjust bubble size smaller for better visibility
                c='b',
                alpha=0.6,  # Add transparency for better visibility
                edgecolors='w',  # Add white border to bubbles
                linewidth=0.5)

    # Add labels for x and y axis and plot title
    plt.xlabel('Country')
    plt.ylabel('Total Sales')  
    plt.title('Bubble Plot Hubungan Wilayah dan Penjualan')

    # Menambahkan grid untuk memudahkan membaca plot
    plt.grid(True)

    # Display plot di Streamlit
    st.markdown("<h2 style='text-align: center;'>Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    st.markdown(""" <p style='color: black;'>
        Dari visualisasi di atas dapat dilihat adanya hubungan antara jumlah penjualan dengan region penjualan, region yang memiliki 
        daerah yang luas dan lebih besar cenderung menghasilkan penjualan produk yang besar pula.</p>
    """,unsafe_allow_html=True)

    # Query data pie chart
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

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.markdown("<p style='color: black; font-size: 18px;'>3. Proporsi Penjualan Berdasarkan Wilayah atau Region</p>", unsafe_allow_html=True)
    st.dataframe(df_sales_by_region)

    # Create visualization of sales proportion per region
    plt.figure(figsize=(10, 6))
    plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
    plt.title('Proporsi Penjualan per Wilayah atau Region')
    plt.axis('equal')  # Make pie chart a circle

    # Display plot di Streamlit
    st.markdown("<h2 style='text-align: center;'>Proporsi Penjualan per Wilayah atau Region</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    st.markdown(""" <p style='color: black;'>
        Dari visualisasi di atas dapat dilihat prosentase penjualan produk dari berbagai region Australia dan southwest memiliki 
        prosentase penjualan tertinggi.</p>
    """,unsafe_allow_html=True)

    # Query data bar chart
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

    # Menampilkan DataFrame di Streamlit sebagai tabel
    st.markdown("<p style='color: black; font-size: 18px;'>4. Komposisi Penjualan Berdasarkan Kategori Produk</p>", unsafe_allow_html=True)
    st.dataframe(df_bar)

    # Membuat figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bar (more suitable than histogram for categories)
    ax.bar(df_bar['ProductCategory'], df_bar['TotalSales'], color='blue')

    # Setting labels        
    ax.set(title='Komposisi Penjualan per Kategori Produk',
           ylabel='Total Penjualan',   
           xlabel='Kategori Produk')

    # Rotate x labels for better readability
    plt.xticks(rotation=45)

    # Display plot di Streamlit
    st.markdown("<h2 style='text-align: center;'>Komposisi Penjualan per Kategori Produk</h2>", unsafe_allow_html=True)
    st.pyplot(fig)

    st.markdown(""" <p style='color: black;'>
        Dari visualisasi di atas dapat dilihat distribusi penjualan berdasarkan dari jenis produknya, penjualan terbesar berasal dari produk sepeda.</p>
    """,unsafe_allow_html=True)

    # Menutup koneksi setelah digunakan
    conn.close()

# Menampilkan informasi data diri
st.markdown("""<p style='text-align: left; color: black; font-size: 14px;'>Nama : Fannia Nur Aziza<br>
                NPM : 21082010170<br>
                Mata Kuliah : Data Visualisasi<br>
                Paralel : B</p>""", unsafe_allow_html=True)

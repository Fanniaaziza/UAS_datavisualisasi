import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk memuat Adventure Works data
def load_adventure_works_data():
    conn = pymysql.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        db=st.secrets["database"]["db"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    query_sales = """
        SELECT CalendarYear AS Year, SUM(factfinance.Amount) AS TotalSales
        FROM dimtime
        JOIN factfinance ON dimtime.TimeKey = factfinance.TimeKey
        GROUP BY CalendarYear
        ORDER BY CalendarYear
    """
    df_sales = pd.read_sql(query_sales, conn)
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

    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']
    if set(expected_columns).issubset(df_imdb.columns):
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

    df_sales = load_adventure_works_data()
    st.markdown("<p style='color: black; font-size: 18px;'>1. Data Penjualan Tahunan</p>", unsafe_allow_html=True)
    st.dataframe(df_sales)

    if not df_sales.empty:
        try:
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)
            df_filtered = df_sales[(df_sales['Year'] >= year_range[0]) & (df_sales['Year'] <= year_range[1])]

            plt.figure(figsize=(12, 6))
            plt.plot(df_filtered['Year'], df_filtered['TotalSales'], marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
            plt.title(f'Perbandingan Total Penjualan Tahun {year_range[0]}-{year_range[1]}', fontsize=16)
            plt.xlabel('Tahun', fontsize=14)
            plt.ylabel('Total Penjualan', fontsize=14)
            plt.grid(True)

            st.markdown(f"<h2 style='text-align: center;'>Grafik Total Penjualan </h2>", unsafe_allow_html=True)
            st.pyplot(plt)

            st.markdown(""" <p style='color: black;'>
            Dari visualisasi di atas dapat dilihat adanya kenaikan penjualan tertinggi di tahun 2003 dan penjualan yang
            """,unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

    query_bubble = '''
    SELECT 
      st.SalesTerritoryRegion AS Country,
      SUM(fs.SalesAmount) AS TotalSales  
    FROM factinternetsales fs
    JOIN dimsalesterritory st ON fs.SalesTerritoryKey = st.SalesTerritoryKey
    GROUP BY st.SalesTerritoryRegion
    ORDER BY TotalSales DESC
    '''
    
    conn = pymysql.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        db=st.secrets["database"]["db"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    df_bubble = pd.read_sql(query_bubble, conn)
    conn.close()
    
    st.markdown("<p style='color: black; font-size: 18px;'>2. Data Penjualan Wilayah</p>", unsafe_allow_html=True)
    st.dataframe(df_bubble)
    
    try:
        fig, ax = plt.subplots(figsize=(14, 8))
        scatter = ax.scatter(df_bubble['Country'], df_bubble['TotalSales'], s=df_bubble['TotalSales']/1000, alpha=0.5, c='blue')
        ax.set_title('Total Penjualan per Wilayah', fontsize=16)
        ax.set_xlabel('Wilayah', fontsize=14)
        ax.set_ylabel('Total Penjualan', fontsize=14)
        ax.grid(True)
        
        st.markdown(f"<h2 style='text-align: center;'>Bubble Chart Penjualan Wilayah</h2>", unsafe_allow_html=True)
        st.pyplot(fig)
        
        st.markdown(""" <p style='color: black;'>
        Dari visualisasi tersebut menggambarkan bahwa negara dengan penjualan terbanyak yaitu Amerika Serikat.</p> 
        """,unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

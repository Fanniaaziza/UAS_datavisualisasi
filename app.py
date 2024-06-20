import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to load Adventure Works data
def load_adventure_works_data():
    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )

    # SQL query to fetch yearly sales data
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

# Function to load IMDB data
def load_imdb_data():
    fn1 = 'IMDB-TOP.csv'
    return pd.read_csv(fn1, encoding='latin1').head(10)  # Using only the first 10 rows

# Streamlit app title
st.title("Final Project Mata Kuliah Data Visualisasi")

# Sidebar option to select data to display
option = st.sidebar.selectbox(
    'Pilih data yang ingin ditampilkan:',
    ('IMDB Top Movies', 'Adventure Works')
)

# Handling IMDB Top Movies data
if option == 'IMDB Top Movies':
    df_imdb = load_imdb_data()
    st.title("Scraping Website IMDB")
    st.write(df_imdb)

    # Check if necessary columns exist
    expected_columns = ['judul', 'tahun', 'durasi', 'age', 'rate']  # Expected columns
    if set(expected_columns).issubset(df_imdb.columns):
        # 1. Comparison Visualization: Number of Movies per Year
        year_counts = df_imdb['tahun'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.index.astype(str), year_counts.values, color='skyblue')
        plt.title('Perbandingan Jumlah Film per Tahun')
        plt.xlabel('Tahun')
        plt.ylabel('Jumlah Film')
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
        Visualisasi ini menggunakan grafik batang untuk menunjukkan bagaimana jumlah film berubah dari tahun ke tahun dalam dataset IMDB-TOP.csv. 
        Grafik ini memberikan gambaran tentang seberapa aktifnya industri film dalam periode waktu yang dianalisis.
        """)
        
        # 2. Relationship Visualization: Scatter Plot of Film Duration vs Rate
        plt.figure(figsize=(10, 6))
        plt.scatter(df_imdb['durasi'], df_imdb['rate'], alpha=0.5, color='orange')
        plt.title('Hubungan Antara Durasi Film dan Rate')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Rate')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
        Scatter plot ini memvisualisasikan hubungan antara durasi film (sumbu x) dan rating IMDb (sumbu y). 
        Setiap titik merepresentasikan satu film dalam dataset. Pada plot ini, kita dapat melihat pola atau tren umum antara durasi film dengan rating IMDb, 
        meskipun tidak terlalu jelas dalam 10 data pertama yang ditampilkan.
        """)
            
        # 3. Distribution Visualization: Histogram of Film Duration Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df_imdb['durasi'], bins=20, color='green', edgecolor='black')
        plt.title('Distribusi Durasi Film')
        plt.xlabel('Durasi Film (Menit)')
        plt.ylabel('Frekuensi')
        plt.grid(True)
        st.pyplot(plt)

        st.markdown("""
        Histogram ini menunjukkan distribusi frekuensi durasi film dalam dataset. 
        Dengan membagi durasi film ke dalam beberapa bin, plot ini memberikan gambaran visual tentang sebaran durasi film yang ada. 
        Warna hijau digunakan untuk menyoroti distribusi ini, sementara garis tepi hitam menambahkan detail visual.
        """)
            
        # 4. Composition Visualization: Pie Chart of Movie Count per Age Rating
        age_counts = df_imdb['age'].value_counts()

        plt.figure(figsize=(8, 8))
        plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Komposisi Film Berdasarkan Age Rating')
        plt.axis('equal')
        st.pyplot(plt)

        st.markdown("""
        Pie chart ini memvisualisasikan komposisi jumlah film berdasarkan rating usia (Age Rating) dalam dataset. 
        Setiap sektor dalam pie chart mewakili persentase dari jumlah total film dalam kategori rating usia yang berbeda. 
        Chart ini membantu kita melihat seberapa beragam usia target penonton untuk film-film dalam dataset.
        """)

    else:
        st.write("Kolom yang diperlukan (judul, tahun, durasi, age, rate) tidak lengkap dalam dataset.")

# Handling Adventure Works data
else:
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Load Adventure Works data
    df_sales = load_adventure_works_data()

    # Display DataFrame in Streamlit as a table
    st.subheader('1. Data Penjualan Tahunan')
    st.dataframe(df_sales)

    # Check if the DataFrame is not empty
    if not df_sales.empty:
        try:
            # Ensure Year column is of integer type
            df_sales['Year'] = pd.to_numeric(df_sales['Year'], errors='coerce').fillna(0).astype(int)
            tahun_options = range(df_sales['Year'].min(), df_sales['Year'].max() + 1)

            # Option to select year range using a slider
            year_range = st.slider('Pilih Rentang Tahun:', min_value=min(tahun_options), max_value=max(tahun_options), value=(min(tahun_options), max(tahun_options)), step=1)

            # Filter data based on selected year range
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
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning('Tidak ada data penjualan tersedia.')

     st.markdown("""
        Dari visualisasi diatas dapat dilihat adanya kenaikan penjualan tertinggi di tahun 2003 dan penjualan yang menurun di tahun 2004.
        """)

    # Query data for bubble plot
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

    # Display DataFrame in Streamlit as a table
    st.subheader('2. Hubungan Penjualan berdasarkan region')
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

    # Add grid for easier reading of the plot
    plt.grid(True)

    # Display plot in Streamlit
    st.markdown("<h2 style='text-align: center;'>Bubble Plot Hubungan Wilayah dan Penjualan</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    st.markdown("""
        Dari visualisasi diatas dapat dilihat adanya hubungan antara jumlah penjualan dengan region penjualan, region yang memiliki 
        daerah yang luas dan lebih besar cenderung menghasilkan penjualan produk yang besar pula.
        """)

    # Query data for pie chart
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

    # Display DataFrame in Streamlit as a table
    st.subheader('3. Proporsi Penjualan Berdasarkan Wilayah atau Region')
    st.dataframe(df_sales_by_region)

    # Create visualization of sales proportion per region
    plt.figure(figsize=(10, 6))
    plt.pie(df_sales_by_region['TotalSales'], labels=df_sales_by_region['SalesTerritoryRegion'], autopct='%1.1f%%', startangle=140)
    plt.title('Proporsi Penjualan per Wilayah atau Region')
    plt.axis('equal')  # Make pie chart a circle

    # Display plot in Streamlit
    st.markdown("<h2 style='text-align: center;'>Proporsi Penjualan per Wilayah atau Region</h2>", unsafe_allow_html=True)
    st.pyplot(plt)

    st.markdown(""" Dari visualisasi diatas dapat dilihat prosentase penjualan produk dari berbagai region Australia dan southwest memiliki 
    prosentase penjualan tertinggi. 
    """)

    # Query data for bar chart
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

    # Display DataFrame in Streamlit as a table
    st.subheader('4. Komposisi Penjualan Berdasarkan Kategori Produk')
    st.dataframe(df_bar)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bar (more suitable than histogram for categories)
    ax.bar(df_bar['ProductCategory'], df_bar['TotalSales'], color='blue')

    # Setting labels        
    ax.set(title='Komposisi Penjualan per Kategori Produk',
           ylabel='Total Penjualan',   
           xlabel='Kategori Produk')

    # Rotate x labels for better readability
    plt.xticks(rotation=45)

    # Display plot in Streamlit
    st.markdown("<h2 style='text-align: center;'>Komposisi Penjualan per Kategori Produk</h2>", unsafe_allow_html=True)
    st.pyplot(fig)

    st.markdown(""" Dari visualisasi diatas dapat dilihat dilihat distribusi penjualan berdasarkan dari jenis produknya, penjualan terbesar berasal dari produk sepeda. 
    """)

    # Close connection after usage
    conn.close()

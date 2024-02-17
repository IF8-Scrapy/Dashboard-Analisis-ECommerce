import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import geopandas as gpd

@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_data_dates(url, dates):
    df = pd.read_csv(url, parse_dates=dates)
    return df

# Menyiapkan data untuk plotting
def load_world():
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    return world

df_customers = load_data('dataset/customers_dataset.csv')
df_order_items = load_data('dataset/order_items_dataset.csv')
df_orders = load_data_dates('dataset/orders_dataset.csv', ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date'])
df_products = load_data('dataset/products_dataset.csv')
df_product_category_name_translation = load_data('dataset/product_category_name_translation.csv')
df_sellers = load_data('dataset/sellers_dataset.csv')
df_order_payments = load_data('dataset/order_payments_dataset.csv')
df_geolocation = load_data('dataset/geolocation_dataset.csv')

def Tab_Audrey(df_order_items):
    st.header("Pertanyaan 1: \"Seller mana yang menjual produk paling banyak (memvisualisasi hanya 5 teratas)?\"")
    # Menghitung jumlah produk yang dijual oleh setiap seller
    jumlah_produk_per_seller = df_order_items['seller_id'].value_counts()

    # Menghitung jumlah penjualan produk per seller
    jumlah_penjualan_per_seller = df_order_items['seller_id'].value_counts().nlargest(5)

    # Menyiapkan data untuk visualisasi
    nama_seller = jumlah_penjualan_per_seller.index.tolist()
    jumlah_penjualan = jumlah_penjualan_per_seller.values.tolist()

    # Membuat grafik histogram jumlah penjualan produk per seller
    fig, ax = plt.subplots()
    ax.bar(nama_seller, jumlah_penjualan, color='blue')
    ax.set_xlabel('id Seller')
    ax.set_ylabel('Jumlah Penjualan')
    plt.xticks(rotation=90, ha='right')

    st.dataframe(jumlah_penjualan_per_seller)
    st.pyplot(fig)

    with st.expander("Penjelasan 5 teratas seller yang menjual produk terbanyak") :
        st.markdown('''**Dapat disimpulkan 5 seller teratas yang menjual produk terbanyak yaitu**:
    1. 6560211a19b47992c3666cc44a7e94c0  jumlah produk terjual 2033
    2. 4a3ca9315b744ce9f8e9374361493884  jumlah produk terjual 1987
    3. 1f50f920176fa81dab994f9023523100  jumlah produk terjual 1931
    4. cc419e0650a3c5ba77189a1882b7556a  jumlah produk terjual 1775
    5. da8622b14eb17ae2831f4ac5b9dab84a  jumlah produk terjual 1551''')
        
    st.write('<hr>', unsafe_allow_html=True)

    st.header("Pertanyaan 2: \"Seller mana yang menjual produk paling banyak (memvisualisasi hanya 5 teratas), lalu seller mana yang menjual produk tersebut dan berapa banyak penghasilan seller tersebut?\"")
    # Menghitung jumlah produk yang dijual oleh setiap seller
    produk_terbanyak = df_order_items['product_id'].value_counts()

    # Menghitung jumlah penjualan produk terbayak
    jumlah_penjualan = df_order_items['product_id'].value_counts()

    # Menyiapkan data untuk visualisasi (di sini, kita akan ambil 5 teratas)
    top_produk = jumlah_penjualan.head(5)
    id_produk = top_produk.index.tolist()
    jumlah_penjualan = top_produk.values.tolist()

    # Membuat plot menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(jumlah_penjualan, labels=id_produk, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Membuat lingkaran menjadi lingkaran sejati (bukan elips)
    ax.set_title('Persentase penjualan produk ter-Laris (Top 5)')

    st.dataframe(produk_terbanyak)
    st.pyplot(fig)

    with st.expander("Penjelasan Penjualan 5 produk terlaris, mencari seller yang menjual produk terlaris dan berapa penghasilan seller tersebut.") :
        st.markdown('''**Dapat disimpulkan 5 produk terlaris yaitu : **:
    1. aca2eb7d00ea1a7b8ebd4e68314663af    527
    2. 99a4788cb24856965c36a24e339b6058    488
    3. 422879e10f46682990de24d770e7f83d    484
    4. 389d119b48cf3043d311335e499d9c6b    392
    5. 368c6c730842d78016ad823897a372db    388''')
        st.markdown('''**Seller yang menjual id produk tersebut adalah : 955fee9216a65b617aa5c0531780ce60**:
    ''')
        st.markdown('''**Penghasilan seller tersebut : 135171.7**:
    ''')
        
    st.write('<hr>', unsafe_allow_html=True)

def Tab_Laras(df_sellers):
    st.header("Pertanyaan 3: \"Negara mana yang memiliki banyak seller dan sedikit sedikit seller?\"")
    # Menghitung jumlah seller dari setiap negara
    jumlah_seller_per_negara = df_sellers['seller_state'].value_counts()
    st.dataframe(jumlah_seller_per_negara)

    
    fig, ax = plt.subplots()
    ax.bar(jumlah_seller_per_negara.index.tolist(), jumlah_seller_per_negara.values.tolist())
    st.pyplot(fig)

    with st.expander("Penjelasan negara dengan seller terbanyak dan sedikit") :
            st.write('Dilihat dari grafik di atas kita dapat menyimpilkan bahwa negara dengan seller terbanyak dan terdikit adalah Negara terbanyak adalah 1. 1849 = SP, 2. 349 = PR, 3. 244 = MG, 4. 190 = SC,5.  171 = RJ, 6. 129 = RS 1. 1 = PA, AM, MA, AC, PI., 2. 2 = RO, SE, 3. 4 = MT, 4. 5 = MS, RN, 5. 6 = PB, 6. 9 = PE, 7. 13 = CE, 8. 19 = BA, 9. 23 = ES, 10. 30 = DF, 11. 40 = GO')




def Tab_Steave(df_customers):
    st.header("Pertanyaan 4: \"10 kota dengan customer terbanyak?\"")

    customers = df_customers['customer_city'].value_counts().nlargest(10)

    fig, ax = plt.subplots()

    ax.bar(customers.index, customers.values)
    plt.xticks(rotation=90, ha='right')

    st.dataframe(customers)
    st.pyplot(fig)

    st.write(
        """
        10 kota dengan customer terbanyak:

Sao paulo,
Rio de jeneiro,
Belo horizonte,
Brasilia,
Curitiba,
Campinas,
Porto Alegre,
Salvador,
Guarulgos,
Sao Bernando Do Campo.
        """
    )

def Tab_Juli(df_order_payments) :

    st.header("ID Order yang sering berbelanja")
    pembayaran_terbanyak = df_order_payments['order_id'].value_counts()

    count_fa65dad1b0e818e3ccc5cb0e39231352= df_order_payments['order_id'].value_counts()['fa65dad1b0e818e3ccc5cb0e39231352']
    count_ccf804e764ed5650cd8759557269dc13 = df_order_payments['order_id'].value_counts()['ccf804e764ed5650cd8759557269dc13']
    count_285c2e15bebd4ac83635ccc563dc71f4  = df_order_payments['order_id'].value_counts()['285c2e15bebd4ac83635ccc563dc71f4']
 
    st.write("Daftar:", pembayaran_terbanyak)

    # Visualisasi Data
    order_id = df_order_payments['order_id'].value_counts()
    jumlah_order = order_id.head()
    payment = jumlah_order.index.tolist()
    order_id = jumlah_order.values.tolist()

    # Membuat Diagram
    fig, ax = plt.subplots()
    ax.plot(payment, order_id, marker='.', color='blue')
    ax.set_xticks(payment)
    ax.set_xticklabels(payment, rotation=90)
    ax.set_title('Data Order ID Terbanyak')
    ax.set_ylabel('Jumlah Order')
    ax.set_xlabel('Order ID')
    st.pyplot(fig)

    # Menganalisis order_id teratas untuk mengetahui payment_value
    order = 'order1'
    order_id_teratas = df_order_payments[df_order_payments['order_id'] == order]

    with st.expander("Penjelasan Metode Pembayarn") :
        st.write('Dilihat dari grafik diatas, 5 Order ID teratas dengan berbelanja terbanyak yaitu Order ID fa65dad1b0e818e3ccc5cb0e39231352 dengan total berbelanja sebanyak 29 kali,Order ID ccf804e764ed5650cd8759557269dc13 dengan total berbelanja sebanyak 26 kali,Order ID 285c2e15bebd4ac83635ccc563dc71f4 dengan total berbelanja sebanyak 22 kali,Order ID 895ab968e7bb0d5659d16cd74cd1650c dengan total berbelanja sebanyak 21 kali,Order ID fedcd9f7ccdc8cba3a18defedd1a5547 dengan total berbelanja sebanyak 19 kali')

    st.write('<hr>', unsafe_allow_html=True) 

    st.header("3 Metode Pembayaran yang sering digunakan")

    count_credit_card = df_order_payments['payment_type'].value_counts()['credit_card']
    count_boleto = df_order_payments['payment_type'].value_counts()['boleto']
    count_voucher = df_order_payments['payment_type'].value_counts()['voucher']

    df_order_payments = pd.DataFrame({
        'Kategori': ['credit_card', 'boleto', 'voucher'],
        'Jumlah': [count_credit_card, count_boleto, count_voucher]
    })

    st.dataframe(df_order_payments)

    # Buat bar chart
    label = df_order_payments['Kategori']
    data = df_order_payments['Jumlah']

    fig, ax = plt.subplots()
    ax.bar(label, data, color=['green' if kategori == 'voucher' else 'red' for kategori in label])
    ax.set_xlabel('Kategori')
    ax.set_ylabel('Jumlah')
    

    #Membuat Diagram Pie
    warna = ['pink','aqua','magenta']
    fig, ax = plt.subplots()
    ax.pie(data, labels=label, autopct='%1.1f%%', startangle=90, colors = warna, shadow =True)
    ax.axis('equal')
    st.markdown('**Metode Pembayaran yang sering digunakan dalam bentuk diagram PIE**')

    st.pyplot(fig)

    with st.expander("Penjelasan Metode Pembayarn") :
        st.write('Dilihat dari gambar PIE diatas, Ada 3 Metode Pembayaran yang paling banyak digunakan yaitu Credit Card dengan jumlah penggunaan 76,795, kemudian yang kedua yaitu Boleto dengan jumlah penggunaannya 19,784 dan yang terakhir yaiut Voucher dengan total penggunaan 5,775.')

    st.write('<hr>', unsafe_allow_html=True) 

def Tab_Dhimas(df_order_payments):
    st.header("Pertanyaan 9: \"Bagaimana perbandingan metode pembayaran yang digunakan oleh seluruh customer?\"")
    Jenis_payment= df_order_payments['payment_type'].value_counts()
 
    fig, ax = plt.subplots()
    ax.bar (Jenis_payment.index.tolist(), Jenis_payment.values.tolist(), color='blue')
    ax.set_xlabel('Jenis Payment')
    ax.set_ylabel('Jumlah Penjualan')

    st.dataframe(Jenis_payment)
    st.pyplot(fig)

def Tab_Raka(df_order_items, df_orders, df_products, df_product_category_name_translation, df_geolocation):
    st.header('10 Kategori Produk Terlaris')
    df_orders_products = df_order_items.set_index('product_id').join(df_products.set_index('product_id'))
    df_translated_category = df_orders_products.set_index('product_category_name').join(df_product_category_name_translation.set_index('product_category_name'))

    top_products = df_translated_category['product_category_name_english'].value_counts().nlargest(10)

    fig, ax = plt.subplots()
    ax.bar(top_products.index, top_products.values)
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Total Penjualan')
    plt.xticks(rotation=90, ha='right')

    st.dataframe(top_products)
    st.pyplot(fig)

    with st.expander("Penjelasan 10 Kategori Produk Terlaris") :
        st.markdown('''**Dapat disimpulkan 10 kategori produk dengan pemesanan terbanyak yaitu**:
1. bed_bath_table
2. health_beauty
3. sports_leisure
4. furniture_decor
5. computers_accesories
6. housewares
7. watches_gifts
8. telephony
9. garden_tools
10. auto''')
        
    st.write('<hr>', unsafe_allow_html=True)
    
    st.header('Tren Penjualan Bulanan untuk Kategori Produk Terlaris tahun 2017-2018')
    # Merge tables
    merged_data = pd.merge(df_order_items, df_orders, on="order_id")
    merged_data = pd.merge(merged_data, df_products, on="product_id")
    merged_data = pd.merge(merged_data, df_product_category_name_translation, on="product_category_name")

    # Extract year and month from order_purchase_timestamp
    merged_data["order_year_month"] = merged_data["order_purchase_timestamp"].dt.to_period("M")

    # Group by product and month, calculate total sales
    product_monthly_sales = merged_data.groupby(["product_id", "order_year_month"]).size().reset_index(name='total_sales')

    # Find the most sold product
    most_sold_product_id = product_monthly_sales.groupby("product_id")["total_sales"].sum().idxmax()

    # Filter data for the most sold product and the desired time frame
    most_sold_product_data = product_monthly_sales[product_monthly_sales["product_id"] == most_sold_product_id]

    # Merge with df_products dataset to get category name
    most_sold_product_data = pd.merge(most_sold_product_data, df_products[['product_id', 'product_category_name']], on='product_id')

    # Merge with df_product_category_name_translation dataset to get category name
    most_sold_product_data = pd.merge(most_sold_product_data, df_product_category_name_translation[['product_category_name', 'product_category_name_english']], on='product_category_name')

    # Convert Period to string for plotting
    most_sold_product_data["order_year_month_str"] = most_sold_product_data["order_year_month"].astype(str)
    
    most_sold_product_category = most_sold_product_data.iloc[0]['product_category_name_english']

    data_tabel = pd.DataFrame({
        "Tahun-Bulan": most_sold_product_data["order_year_month_str"],
        "Total Penjualan": most_sold_product_data["total_sales"]
    })

    fig, ax = plt.subplots()
    ax.plot(most_sold_product_data["order_year_month_str"], most_sold_product_data["total_sales"], marker='o')
    ax.set_title(f'Penjualan Bulanan untuk Kategori Produk Terlaris ({most_sold_product_category}) Tahun 2017 - 2018')
    ax.set_xlabel('Tahun-Bulan')
    ax.set_ylabel('Total Penjualan')
    ax.grid(True)
    plt.xticks(rotation=90, ha='right')

    st.dataframe(data_tabel)
    st.pyplot(fig)

    with st.expander("Penjelasan Tren Penjualan Bulanan") :
        st.markdown('''**Kategori produk terlaris selama tahun 2017-2018 adalah furniture_decor dengan tren penjualan bulanan sebagai berikut:**
- 2017-11 terjadi kenaikan penjualan melebihi 750%, mencapai angka 40
- 2018-01 terjadi kenaikan penjualan sekitar 200% dan merupakan puncak penjualan tahun 2017-2018, mencapai angka 120
- 2018-02 terjadi penurunan penjualan sebanyak 70%, mencapai angka 40 dan terus meningkat setiap bulannya hingga 2018-05, mencapai angka 90 sebelum hampir tidak ada penjualan sama sekali setelahnya''')
        
    st.write('<hr>', unsafe_allow_html=True)

    st.header('Persebaran Lokasi yang Terdaftar')

    # Membuat GeoDataFrame dari data
    gdf = gpd.GeoDataFrame(df_geolocation, geometry=gpd.points_from_xy(df_geolocation['geolocation_lng'], df_geolocation['geolocation_lat']))

    grouped_data = df_geolocation.groupby('geolocation_state').size().reset_index(name='count')
    grouped_data = grouped_data.sort_values(by='count', ascending=False)
    st.dataframe(grouped_data)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 10))
    world = load_world()
    world.plot(ax=ax, color='lightgrey', edgecolor='black')
    gdf.plot(ax=ax, markersize=5, color='red', alpha=0.5)
    st.pyplot(fig)

    with st.expander("Penjelasan Persebaran Lokasi") :
        st.markdown('''Hampir semua yang terdaftar berasal dari negara Brasil, dengan mayoritas berasal dari negara bagian Sao Paulo(SP), Minas Gerais(MG), dan Rio de Janeiro(RJ).''')



with st.sidebar :
    selected = option_menu('Menu',['Dashboard'],
    icons =["easel2", "graph-up"],
    menu_icon="cast",
    default_index=0)
    
if (selected == 'Dashboard') :
    st.header(f"Dashboard Analisis E-Commerce")
    st.header("Kelompok Scrapy - IF8")
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["10122283- Audrey", "10122285 - Laras", "10122302 - Steave", "10122303 - Juli", "10122309 - Dhimas Kurnia", "10122301 - Raka"])

    with tab1 :
        Tab_Audrey(df_order_items)
    with tab2 :
        Tab_Laras(df_sellers)
    with tab3 :
        Tab_Steave(df_customers)
    with tab4 :
        Tab_Juli(df_order_payments)
    with tab5 :
        Tab_Dhimas(df_order_payments)
    with tab6 :
        Tab_Raka(df_order_items, df_orders, df_products, df_product_category_name_translation, df_geolocation)

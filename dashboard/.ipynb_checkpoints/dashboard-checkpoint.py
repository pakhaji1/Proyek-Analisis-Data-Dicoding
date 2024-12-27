import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import streamlit as st

# Fungsi untuk membaca data
def load_data():
    data_df = pd.read_csv('D:/folder kiki/dicoding/Proyek Analisis Data Dicoding/dashboard/dashboard.csv')
    data_df['dteday'] = pd.to_datetime(data_df['dteday']) 
    return data_df

# Fungsi untuk visualisasi penyewaan sepeda berdasarkan rentang waktu
def rentals_tahun(data_df):
    # Menggunakan variabel global untuk start_date dan end_date
    global start_date, end_date
    rentals_year = data_df[(data_df['dteday'] >= pd.to_datetime(start_date)) & (data_df['dteday'] <= pd.to_datetime(end_date))]  # Memfilter data berdasarkan rentang tanggal
    rentals_year.set_index('dteday', inplace=True)
    monthly_rentals = rentals_year.resample('ME').sum()

    plt.figure(figsize=(20, 15))
    plt.plot(monthly_rentals.index, monthly_rentals['cnt'], marker='o', color='skyblue')
    plt.title(f"Jumlah Penyewaan Sepeda dari {start_date} hingga {end_date}", fontsize=20)
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewa")
    plt.xticks(monthly_rentals.index, monthly_rentals.index.strftime('%B %Y'), rotation=30)
    plt.grid(True)
    st.pyplot(plt)

# Fungsi untuk visualisasi penyewaan sepeda per musim
def rentals_musim(data_df):
    total_rentals = data_df.groupby('season')['cnt'].sum().reset_index()

    # Membuat daftar warna untuk setiap bar
    colors = ['skyblue'] * len(total_rentals)  # Warna default untuk semua bar
    max_index = total_rentals['cnt'].idxmax()  # Indeks bar dengan penyewaan tertinggi
    colors[max_index] = 'blue'  # Ubah warna bar tertinggi

    plt.figure(figsize=(10, 5))
    plt.title('Total Penyewaan Sepeda Setiap Musim', fontsize=20)
    bars = plt.bar(total_rentals['season'], total_rentals['cnt'], color=colors)
    plt.xlabel('Musim')
    plt.ylabel('Total Penyewaan')

    # Menambahkan nilai total penyewaan di atas setiap bar
    for bar in bars:
        yval = bar.get_height()  # Mendapatkan tinggi bar
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')  # Menambahkan teks
    
    # Mengatur label sumbu X secara manual
    plt.xticks(ticks=total_rentals['season'], labels=total_rentals['season'])
    
    # Mengatur batas sumbu Y
    plt.ylim(0, total_rentals['cnt'].max() * 1.1)  # Menambahkan sedikit ruang di atas bar
    
    # Mengatur format angka pada sumbu Y
    def millions(x, pos):
        return '%1.0f' % (x)
    
    formatter = FuncFormatter(millions)
    plt.gca().yaxis.set_major_formatter(formatter)
    st.pyplot(plt)

# Fungsi untuk visualisasi perbandingan penyewaan di hari kerja dan akhir pekan
def rentals_weekday_weekend(data_df):
    total_rentals_weekday = data_df.groupby('workingday')['cnt'].sum().reset_index()
    total_rentals_weekday['day_type'] = total_rentals_weekday['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

    plt.figure(figsize=(10, 5))
    plt.pie(total_rentals_weekday['cnt'], labels=total_rentals_weekday['day_type'], autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen'])
    plt.title('Perbandingan Penyewaan Sepeda di Hari Kerja dan Akhir Pekan', fontsize=20)
    st.pyplot(plt)

# Fungsi untuk visualisasi penyewaan sepeda per musim
def rentals_cuaca(data_df):
    total_rentals = data_df.groupby('weathersit')['cnt'].sum().reset_index()

    # Membuat daftar warna untuk setiap bar
    colors = ['green'] * len(total_rentals)  # Warna default untuk semua bar
    max_index = total_rentals['cnt'].idxmax()  # Indeks bar dengan penyewaan tertinggi
    colors[max_index] = 'lightblue'  # Ubah warna bar tertinggi

    plt.figure(figsize=(10, 5))
    plt.title('Total Penyewaan Sepeda Setiap Cuaca', fontsize=20)
    bars = plt.bar(total_rentals['weathersit'], total_rentals['cnt'], color=colors)
    plt.xlabel('Cuaca')
    plt.ylabel('Total Penyewaan')

        # Menambahkan nilai total penyewaan di atas setiap bar
    for bar in bars:
        yval = bar.get_height()  # Mendapatkan tinggi bar
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')  # Menambahkan teks
    
        # Mengatur label sumbu X secara manual
    plt.xticks(ticks=total_rentals['weathersit'], labels=total_rentals['weathersit'])
    
    # Mengatur batas sumbu Y
    plt.ylim(0, total_rentals['cnt'].max() * 1.1)  # Menambahkan sedikit ruang di atas bar
    
    # Mengatur format angka pada sumbu Y
    def millions(x, pos):
        return '%1.0f' % (x)
    
    formatter = FuncFormatter(millions)
    plt.gca().yaxis.set_major_formatter(formatter)
    st.pyplot(plt)

# Judul Dashboard
st.title('Proyek Analisis Data Dashboard Penyewaan Sepeda')

# Memuat data
data_df = load_data()

# Menentukan min dan max tanggal
min_date = data_df['dteday'].min()
max_date = data_df['dteday'].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("D:/folder kiki/dicoding/Proyek Analisis Data Dicoding/dashboard/rentalsepeda.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

# Memfilter data berdasarkan rentang tanggal yang dipilih
main_df = data_df[(data_df['dteday'] >= pd.to_datetime(start_date)) & 
                   (data_df['dteday'] <= pd.to_datetime(end_date))]

# Visualisasi penyewaan sepeda berdasarkan rentang tahun yang dipilih
st.subheader(f"1. Bagaimana kondisi penyewaan sepeda dari tahun {start_date} hingga {end_date}?")
rentals_tahun(main_df)

# Visualisasi penyewaan sepeda per musim
st.subheader("2. Pada musim apa penyewaan sepeda terbanyak?")
rentals_musim(main_df)

# Visualisasi perbandingan penyewaan di hari kerja dan akhir pekan
st.subheader("3. Bagaimana perbandingan penyewaan sepeda di hari kerja dengan akhir pekan?")
rentals_weekday_weekend(main_df)

st.subheader("Perbandingan Berdasarkan Cuaca")
rentals_by_cuaca(main_df)

st.caption('Copyright © Muhammad Rizeky Rahmatullah 2024')









    


    

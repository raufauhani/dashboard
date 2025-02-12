import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_day = pd.read_csv("data/day.csv")
data_hour = pd.read_csv("data/hour.csv")

# Konversi kolom tanggal ke format datetime
data_day['dteday'] = pd.to_datetime(data_day['dteday'])

# Mendapatkan rentang tanggal untuk filter
min_date = data_day['dteday'].min()
max_date = data_day['dteday'].max()

# Mapping musim agar lebih mudah dibaca
data_day['season'] = data_day['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
data_hour['season'] = data_hour['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

# Mapping weekday agar lebih mudah dibaca
day_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
data_day['weekday'] = data_day['weekday'].map(day_mapping)

# Dashboard title
st.title("Dashboard Bike Sharing")

# Sidebar
with st.sidebar:
    # Logo
    st.image("https://i.pinimg.com/736x/17/3c/8e/173c8e1a393602c7eb0aa963e4af3f71.jpg", use_container_width=True)
    
    # Judul filter
    st.title("Filter Data")

    # Rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter Musim
    season_filter = st.multiselect("Select season:", options=data_day['season'].unique(), default=data_day['season'].unique())
    
    # Filter Hari
    day_filter = st.multiselect("Select weekday:", options=data_day['weekday'].unique(), default=data_day['weekday'].unique())

# Filter data berdasarkan pilihan pengguna
filtered_data_day = data_day[
    (data_day['season'].isin(season_filter)) & 
    (data_day['dteday'].between(pd.Timestamp(start_date), pd.Timestamp(end_date))) &
    (data_day['weekday'].isin(day_filter))
]

# Menampilkan data yang difilter
st.write("Data yang Ditampilkan:", filtered_data_day)

# Visualisasi 1: Penyewaan Sepeda Berdasarkan Musim
st.subheader("1. Apakah ada perbedaan signifikan dalam penggunaan sepeda di setiap musim?")
st.subheader("Jumlah Penyewaan Berdasarkan Musim")
fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_data_day, x='season', y='cnt', ax=ax1)
ax1.set_title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig1)

# Visualisasi 2: Penyewaan Sepeda Berdasarkan Hari Kerja
st.subheader("2. Bagaimana penggunaan sepeda lebih tinggi pada hari kerja tertentu (weekday)?")
st.subheader("Jumlah Penyewaan Berdasarkan Hari Kerja")
fig2, ax2 = plt.subplots()
sns.barplot(data=filtered_data_day, x='weekday', y='cnt', ax=ax2, order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
ax2.set_title("Penyewaan Sepeda Berdasarkan Hari Kerja")
st.pyplot(fig2)

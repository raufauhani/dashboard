import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_day = pd.read_csv("../data/day.csv")
data_hour = pd.read_csv("../data/hour.csv")

# Konversi kolom tanggal ke format datetime
data_day['dteday'] = pd.to_datetime(data_day['dteday'])

# Mendapatkan rentang tanggal untuk filter
min_date = data_day['dteday'].min()
max_date = data_day['dteday'].max()

# Mapping musim agar lebih mudah dibaca
data_day['season'] = data_day['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
data_hour['season'] = data_hour['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

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

    # Filter Hari untuk cek kolom weekday 
    if 'weekday' in data_day.columns:
        day_filter = st.multiselect("Select day:", options=data_day['weekday'].unique(), default=data_day['weekday'].unique())
    else:
        day_filter = []

# Filter data berdasarkan pilihan pengguna
filtered_data_day = data_day[
    (data_day['season'].isin(season_filter)) & 
    (data_day['dteday'].between(pd.Timestamp(start_date), pd.Timestamp(end_date)))
]


if day_filter:
    filtered_data_day = filtered_data_day[filtered_data_day['weekday'].isin(day_filter)]

# Menampilkan data yang difilter
st.write("Data yang Ditampilkan:", filtered_data_day)

# Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader("Jumlah Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots()
sns.barplot(data=filtered_data_day, x='season', y='cnt', ax=ax)
plt.title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

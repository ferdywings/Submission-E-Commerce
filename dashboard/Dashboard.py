import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r"D:\Submission_Ferdy\Dashboard\all_data.csv"
df = pd.read_csv(file_path)

df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], format='mixed', errors='coerce')
df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], format='mixed', errors='coerce')

st.title("📊 E-Commerce Dashboard")
st.markdown("### Dashboard yang menarik dan interaktif untuk memantau performa e-commerce.")

st.sidebar.header("🔍 Filter")
selected_category = st.sidebar.multiselect("Pilih Kategori Produk", df['product_category_name_english'].dropna().unique())
selected_payment = st.sidebar.multiselect("Pilih Metode Pembayaran", df['payment_type'].dropna().unique())
selected_review_score = st.sidebar.slider("Pilih Skor Review Minimum", min_value=int(df['review_score'].min()), max_value=int(df['review_score'].max()), value=int(df['review_score'].min()))
selected_price_range = st.sidebar.slider("Pilih Rentang Harga", min_value=float(df['price'].min()), max_value=float(df['price'].max()), value=(float(df['price'].min()), float(df['price'].max())))

if selected_category:
    df = df[df['product_category_name_english'].isin(selected_category)]
if selected_payment:
    df = df[df['payment_type'].isin(selected_payment)]
df = df[df['review_score'] >= selected_review_score]
df = df[(df['price'] >= selected_price_range[0]) & (df['price'] <= selected_price_range[1])]

st.subheader("📈 Metrik Utama")
col1, col2, col3 = st.columns(3)
total_sales = df['price'].sum()
total_orders = df['order_id'].nunique()
total_customers = df['seller_id'].nunique()
col1.metric("Total Penjualan", f"${total_sales:,.2f}")
col2.metric("Total Pesanan", total_orders)
col3.metric("Total Penjual", total_customers)

st.subheader("📊 Tren Penjualan dari Waktu ke Waktu")
st.markdown("Grafik ini menunjukkan tren total penjualan dari waktu ke waktu, membantu mengidentifikasi tren musiman dan pertumbuhan bisnis.")
df['order_date'] = df['shipping_limit_date'].dt.to_period("M")
sales_trend = df.groupby('order_date')['price'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x=sales_trend['order_date'].astype(str), y=sales_trend['price'], marker='o', ax=ax)
ax.set_title("Tren Penjualan Bulanan")
ax.set_xlabel("Tanggal Pesanan")
ax.set_ylabel("Total Penjualan")
plt.xticks(rotation=45)
st.pyplot(fig)

with st.expander("🏆 Produk Terlaris"):
    st.markdown("Grafik batang ini menampilkan 10 kategori produk dengan penjualan tertinggi berdasarkan total penjualan.")
    top_products = df.groupby('product_category_name_english')['price'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=top_products['price'], y=top_products['product_category_name_english'], palette='coolwarm', ax=ax)
    ax.set_title("10 Kategori Produk Terlaris")
    ax.set_xlabel("Total Penjualan")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

with st.expander("💳 Distribusi Metode Pembayaran"):
    st.markdown("Grafik ini memberikan wawasan tentang distribusi berbagai metode pembayaran yang digunakan oleh pelanggan.")
    payment_counts = df['payment_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='viridis', ax=ax)
    ax.set_title("Metode Pembayaran yang Digunakan")
    ax.set_xlabel("Jenis Pembayaran")
    ax.set_ylabel("Jumlah Pengguna")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with st.expander("🌟 Analisis Review Pelanggan"):
    st.markdown("Bagian ini menyajikan analisis review pelanggan, membantu bisnis memahami tingkat kepuasan pelanggan.")
    avg_review = df['review_score'].mean()
    st.metric("Skor Review Rata-rata", f"{avg_review:.2f}")
    
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(x=df['review_score'], palette='Blues', ax=ax)
    ax.set_title("Distribusi Skor Review")
    ax.set_xlabel("Skor Review")
    ax.set_ylabel("Jumlah Review")
    st.pyplot(fig)
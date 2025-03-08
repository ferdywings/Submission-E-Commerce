import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
orders_df = pd.read_csv("order_sharing_data.csv")
payments_df = pd.read_csv("payments_sharing_data.csv")
product_category_df = pd.read_csv("product_category_sharing_data.csv")
products_df = pd.read_csv("products_sharing_data.csv")
reviews_df = pd.read_csv("reviews_sharing_data.csv")

# Calculate total sales
total_sales = orders_df["price"].sum()

# Count payment methods
payment_counts = payments_df["payment_type"].value_counts()

# Merge order and product data
merged_orders_products = orders_df.merge(products_df, on="product_id", how="left")
merged_orders_products = merged_orders_products.merge(product_category_df, 
                                                       left_on="product_category_name", 
                                                       right_on="product_category_name", 
                                                       how="left")
# Calculate top product categories
category_sales = merged_orders_products.groupby("product_category_name_english")["price"].sum().nlargest(10)

# Count review scores
review_scores = reviews_df["review_score"].value_counts().sort_index()

# Streamlit Sidebar
st.sidebar.title("E-commerce Dashboard")
page = st.sidebar.radio("Select a section:", ["Overview", "Payment Methods", "Top Categories", "Review Scores"])

st.sidebar.markdown("### Metrics")
st.sidebar.metric(label="Total Sales", value=f"${total_sales:,.2f}")

# Streamlit Main Content
st.title("E-commerce Dashboard")

if page == "Overview":
    st.subheader("Total Sales")
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

elif page == "Payment Methods":
    st.subheader("Payment Methods Used")
    st.bar_chart(payment_counts)

elif page == "Top Categories":
    st.subheader("Top 10 Product Categories by Sales")
    fig, ax = plt.subplots()
    sns.barplot(y=category_sales.index, x=category_sales.values, ax=ax, palette="coolwarm")
    ax.set_xlabel("Sales")
    st.pyplot(fig)

elif page == "Review Scores":
    st.subheader("Review Score Distribution")
    fig, ax = plt.subplots()
    sns.barplot(x=review_scores.index, y=review_scores.values, ax=ax, palette="magma")
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Count")
    st.pyplot(fig)
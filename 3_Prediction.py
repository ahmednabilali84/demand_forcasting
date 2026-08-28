import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import date

st.set_page_config(page_title="Prediction", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff !important;
    }
    h1, h2, h3 { color: #00d4ff !important; }

    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label,
    [data-testid="stWidgetLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(90deg, #1a2980, #26d0ce);
        padding: 15px 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .stButton > button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        transform: scale(1.03);
    }

    /* Sidebar white */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141e30, #243b55) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("demand_forecast_model.pkl")

model = load_model()

st.markdown("<h1 style='text-align: center;'>🔮 Demand Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0e7ff; font-size:18px;'>Predict daily product demand for a selected period</p>", unsafe_allow_html=True)
st.markdown("---")

st.header("🛍️ Store & Product Information")
col1, col2, col3 = st.columns(3)

with col1:
    store_id = st.selectbox("Store ID", ["S001", "S002", "S003", "S004", "S005"])
    product_id = st.selectbox("Product ID", [f"P{str(i).zfill(4)}" for i in range(1, 21)])

with col2:
    category = st.selectbox("Category", ["Electronics", "Clothing", "Groceries", "Toys", "Furniture"])
    region = st.selectbox("Region", ["North", "South", "East", "West"])

with col3:
    weather = st.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy", "Snowy"])
    seasonality = st.selectbox("Seasonality", ["Winter", "Spring", "Summer", "Autumn"])

st.header("💰 Pricing & Promotion")
col4, col5, col6 = st.columns(3)

with col4:
    price = st.number_input("Price ($)", min_value=5.0, max_value=250.0, value=65.0, step=0.5)
    competitor_price = st.number_input("Competitor Price ($)", min_value=5.0, max_value=250.0, value=70.0, step=0.5)

with col5:
    discount = st.selectbox("Discount (%)", [0, 5, 10, 15, 20, 25], index=2)
    promotion = st.selectbox("Promotion Active?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

with col6:
    inventory = st.number_input("Inventory Level", min_value=0, max_value=3000, value=220)
    epidemic = st.selectbox("Epidemic?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

st.header("📅 Period Information")
col7, col8 = st.columns(2)

with col7:
    from_date = st.date_input("From Date", value=date(2024, 6, 1))

with col8:
    to_date = st.date_input("To Date", value=date(2024, 6, 7))

if to_date < from_date:
    st.error("To Date must be after From Date")
    st.stop()

st.markdown("---")
st.header("🔮 Prediction")

if st.button("🚀 Predict Demand for the Period", use_container_width=True):
    with st.spinner("Calculating demand for every day in the period..."):
        date_range = pd.date_range(start=from_date, end=to_date, freq="D")
        predictions = []

        for single_date in date_range:
            year = single_date.year
            month = single_date.month
            day = single_date.day
            day_of_week = single_date.dayofweek
            week_of_year = int(single_date.isocalendar()[1])
            is_weekend = 1 if day_of_week >= 5 else 0
            is_month_start = 1 if day <= 5 else 0
            is_month_end = 1 if day >= 25 else 0
            price_diff = price - competitor_price
            price_ratio = price / (competitor_price + 1e-5)

            row = pd.DataFrame({
                "Store ID": [store_id],
                "Product ID": [product_id],
                "Category": [category],
                "Region": [region],
                "Inventory Level": [inventory],
                "Price": [price],
                "Discount": [discount],
                "Weather Condition": [weather],
                "Promotion": [promotion],
                "Competitor Pricing": [competitor_price],
                "Seasonality": [seasonality],
                "Epidemic": [epidemic],
                "Year": [year],
                "Month": [month],
                "Day": [day],
                "DayOfWeek": [day_of_week],
                "IsWeekend": [is_weekend],
                "WeekOfYear": [week_of_year],
                "Price_Diff": [price_diff],
                "Price_Ratio": [price_ratio],
                "Is_Month_Start": [is_month_start],
                "Is_Month_End": [is_month_end],
            })

            pred = model.predict(row)[0]
            predictions.append({
                "Date": single_date.strftime("%Y-%m-%d"),
                "Day Name": single_date.strftime("%A"),
                "Predicted Demand": round(pred, 1),
            })

        results_df = pd.DataFrame(predictions)
        total_demand = results_df["Predicted Demand"].sum()
        avg_demand = results_df["Predicted Demand"].mean()

    st.success(f"### Total Predicted Demand for the Period: **{total_demand:.0f} units**")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Demand", f"{total_demand:.0f} units")
    m2.metric("Average Daily Demand", f"{avg_demand:.1f} units")
    m3.metric("Number of Days", f"{len(results_df)} days")

    st.subheader("📅 Daily Predictions")
    st.dataframe(results_df, use_container_width=True)
    st.bar_chart(results_df.set_index("Date")["Predicted Demand"])

    c1, c2, c3 = st.columns(3)
    c1.success(f"**Store:** {store_id}")
    c2.info(f"**Product:** {product_id} ({category})")
    c3.warning(f"**Promotion:** {'Active' if promotion == 1 else 'None'}")
    st.balloons()

else:
    st.info("Fill in all the fields above, then click **Predict Demand for the Period**.")
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -----------------------------------------
# Page Config + Colorful CSS
# -----------------------------------------
st.set_page_config(
    page_title="Demand Forecasting App",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }

    /* Main titles */
    h1, h2, h3 {
        color: #00d4ff !important;
    }

    /* ===== MAKE ALL INPUT LABELS WHITE ===== */
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Also target Streamlit's specific label class */
    .stSelectbox label, 
    .stNumberInput label,
    .stSlider label,
    .stRadio label,
    [data-testid="stWidgetLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Metric card */
    div[data-testid="stMetric"] {
        background: linear-gradient(90deg, #1a2980, #26d0ce);
        padding: 15px 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Predict button */
    .stButton > button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
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

    .stSuccess {
        background-color: #00b09b;
        color: white;
        border-radius: 12px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Load Model
# -----------------------------------------
@st.cache_resource
def load_model():
    return joblib.load('demand_forecast_model.pkl')

model = load_model()

# -----------------------------------------
# Header
# -----------------------------------------
st.markdown("<h1 style='text-align: center;'>📈 Retail Demand Forecasting</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0e7ff; font-size:18px;'>Predict daily product demand using Machine Learning</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------
# Input Section (No Sidebar)
# -----------------------------------------
st.header("🛍️ Store & Product Information")

col1, col2, col3 = st.columns(3)

with col1:
    store_id = st.selectbox("Store ID", ['S001', 'S002', 'S003', 'S004', 'S005'])
    product_id = st.selectbox("Product ID", [f'P{str(i).zfill(4)}' for i in range(1, 21)])

with col2:
    category = st.selectbox("Category", ['Electronics', 'Clothing', 'Groceries', 'Toys', 'Furniture'])
    region = st.selectbox("Region", ['North', 'South', 'East', 'West'])

with col3:
    weather = st.selectbox("Weather Condition", ['Sunny', 'Cloudy', 'Rainy', 'Snowy'])
    seasonality = st.selectbox("Seasonality", ['Winter', 'Spring', 'Summer', 'Autumn'])

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

st.header("📅 Date Information")

col7, col8, col9, col10 = st.columns(4)

with col7:
    year = st.number_input("Year", min_value=2022, max_value=2026, value=2024)

with col8:
    month = st.number_input("Month", min_value=1, max_value=12, value=6)

with col9:
    day = st.number_input("Day", min_value=1, max_value=31, value=15)

with col10:
    day_of_week = st.number_input("Day of Week (0 = Monday)", min_value=0, max_value=6, value=2)
    week_of_year = st.number_input("Week of Year", min_value=1, max_value=53, value=24)

# -----------------------------------------
# Feature Engineering (same as training)
# -----------------------------------------
is_weekend = 1 if day_of_week >= 5 else 0
is_month_start = 1 if day <= 5 else 0
is_month_end = 1 if day >= 25 else 0
price_diff = price - competitor_price
price_ratio = price / (competitor_price + 1e-5)

input_data = pd.DataFrame({
    'Store ID': [store_id],
    'Product ID': [product_id],
    'Category': [category],
    'Region': [region],
    'Inventory Level': [inventory],
    'Price': [price],
    'Discount': [discount],
    'Weather Condition': [weather],
    'Promotion': [promotion],
    'Competitor Pricing': [competitor_price],
    'Seasonality': [seasonality],
    'Epidemic': [epidemic],
    'Year': [year],
    'Month': [month],
    'Day': [day],
    'DayOfWeek': [day_of_week],
    'IsWeekend': [is_weekend],
    'WeekOfYear': [week_of_year],
    'Price_Diff': [price_diff],
    'Price_Ratio': [price_ratio],
    'Is_Month_Start': [is_month_start],
    'Is_Month_End': [is_month_end]
})

# -----------------------------------------
# Prediction Section
# -----------------------------------------
st.markdown("---")
st.header("🔮 Prediction")

if st.button("🚀 Predict Demand", use_container_width=True):
    with st.spinner("Calculating demand..."):
        prediction = model.predict(input_data)[0]

    st.metric(
        label="Predicted Daily Demand",
        value=f"{prediction:.0f} units"
    )

    c1, c2, c3 = st.columns(3)
    c1.success(f"**Store:** {store_id}")
    c2.info(f"**Product:** {product_id} ({category})")
    c3.warning(f"**Promotion:** {'Active' if promotion == 1 else 'None'}")

    st.balloons()

    with st.expander("📋 View full input data"):
        st.dataframe(input_data.T.rename(columns={0: "Value"}))

else:
    st.info("Fill in all the fields above, then click the **Predict Demand** button.")

# -----------------------------------------
# Footer
# -----------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #88c0d0;'>Built with ❤️ using Streamlit & XGBoost | Retail Demand Forecasting Project</p>",
    unsafe_allow_html=True
)
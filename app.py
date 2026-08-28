import streamlit as st

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff !important;
    }
    h1, h2, h3 { color: #00d4ff !important; }
    p, span, label, div, li { color: #ffffff !important; }

    /* Sidebar */
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

    .stButton > button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📈 Retail Demand Forecasting</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0e7ff; font-size:18px;'>Machine Learning system that predicts daily product demand</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
### About the Project

This application forecasts **daily demand** for products across retail stores using:

- Store & product information  
- Pricing, discounts and promotions  
- Inventory level  
- Weather, seasonality and epidemic signals  

**Goal:** help stores reduce stock-outs and overstock by predicting demand more accurately.

### How to use this app

Use the **sidebar** to navigate:

1. **Data Insights** → Explore patterns in the data  
2. **Model Performance** → See how models were trained and compared  
3. **Prediction** → Enter inputs and get demand forecasts for a period  

### Tech Stack
- Python, Pandas, Scikit-learn, XGBoost  
- Plotly for analysis charts  
- Streamlit for the web interface  
""")

st.markdown("---")
st.caption("Retail Demand Forecasting")

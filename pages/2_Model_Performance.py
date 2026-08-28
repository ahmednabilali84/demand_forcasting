import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Model Performance", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff !important;
    }
    h1, h2, h3 { color: #00d4ff !important; }
    p, span, label, div, li { color: #ffffff !important; }

    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
    }

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

st.markdown("<h1 style='text-align: center;'>🧠 Model Performance</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0e7ff;'>Training, Cross-Validation, Tuning and Final Comparison</p>", unsafe_allow_html=True)
st.markdown("---")

k1, k2, k3 = st.columns(3)
k1.metric("Best Model", "XGBoost (tuned)")
k2.metric("Best R²", "93.14%")
k3.metric("Best MAE", "8.20")

st.markdown("---")

def style_fig(fig, title):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#00d4ff",
        title=title,
        xaxis=dict(color="#ffffff", gridcolor="rgba(255,255,255,0.15)"),
        yaxis=dict(color="#ffffff", gridcolor="rgba(255,255,255,0.15)"),
        legend=dict(font=dict(color="#ffffff"))
    )
    return fig

# 1. Original
st.subheader("1. Original Models (before tuning)")
original_df = pd.DataFrame({
    "Model": ["XGBoost", "Random Forest", "Decision Tree", "Linear Regression",
              "Ridge", "Lasso", "ElasticNet", "KNN Regressor"],
    "MAE": [16.371, 20.988, 22.584, 26.450, 26.450, 26.513, 27.670, 28.539],
    "RMSE": [22.752, 28.570, 30.441, 34.288, 34.289, 34.417, 35.689, 36.653],
    "R2": [76.56, 63.04, 58.04, 46.77, 46.76, 46.37, 42.33, 39.17]
})
st.dataframe(original_df, use_container_width=True)

fig = px.bar(original_df.sort_values("R2"), x="R2", y="Model", orientation="h",
             color="R2", color_continuous_scale="Teal")
st.plotly_chart(style_fig(fig, "R² - Original Models"), use_container_width=True)

# 2. CV
st.subheader("2. 5-Fold Cross-Validation")
cv_df = pd.DataFrame({
    "Model": ["XGBoost", "Random Forest", "Decision Tree", "Linear Regression",
              "Ridge", "Lasso", "ElasticNet", "KNN Regressor"],
    "CV_R2_Mean": [75.65, 62.19, 56.08, 45.41, 45.41, 45.21, 41.49, 37.48],
    "CV_MAE_Mean": [16.603, 21.152, 22.910, 26.710, 26.710, 26.720, 27.776, 28.866]
})
st.dataframe(cv_df, use_container_width=True)

fig = px.bar(cv_df.sort_values("CV_R2_Mean"), x="CV_R2_Mean", y="Model", orientation="h",
             color="CV_R2_Mean", color_continuous_scale="Teal")
st.plotly_chart(style_fig(fig, "CV R² Mean (5-Fold)"), use_container_width=True)

# 3. Tuned
st.subheader("3. After Hyperparameter Tuning (Final Test Set)")
tuned_df = pd.DataFrame({
    "Model": ["XGBoost (tuned)", "Random Forest (tuned)", "Ridge (tuned)"],
    "MAE": [8.200, 15.104, 26.450],
    "RMSE": [12.309, 21.951, 34.290],
    "R2": [93.1395, 78.1821, 46.7619]
})
st.dataframe(tuned_df, use_container_width=True)

fig = px.bar(tuned_df.sort_values("R2"), x="R2", y="Model", orientation="h",
             color="R2", color_continuous_scale="Teal")
st.plotly_chart(style_fig(fig, "R² - Tuned Models"), use_container_width=True)

st.success("**Best Model: XGBoost (tuned)** — R² improved from 76.56% to **93.14%** after tuning.")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Insights", page_icon="📊", layout="wide")

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

@st.cache_data
def load_data():
    return pd.read_csv("demand_forecasting.csv")

df = load_data()

st.markdown("<h1 style='text-align: center;'>📊 Data Insights</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0e7ff;'>Explore patterns that affect product demand</p>", unsafe_allow_html=True)
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Records", f"{len(df):,}")
c2.metric("Avg Demand", f"{df['Demand'].mean():.1f}")
c3.metric("Stores", df['Store ID'].nunique())
c4.metric("Products", df['Product ID'].nunique())

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

st.subheader("Demand Distribution")
fig = px.histogram(df, x="Demand", nbins=40)
st.plotly_chart(style_fig(fig, "Distribution of Daily Demand"), use_container_width=True)

st.subheader("Average Demand by Category")
cat_demand = df.groupby("Category")["Demand"].mean().sort_values(ascending=False).reset_index()
fig = px.bar(cat_demand, x="Category", y="Demand", text_auto=".1f", color="Demand",
             color_continuous_scale="Teal")
st.plotly_chart(style_fig(fig, "Average Demand by Category"), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Demand vs Promotion")
    fig = px.box(df, x="Promotion", y="Demand",
                 labels={"Promotion": "Promotion (0=No, 1=Yes)"})
    st.plotly_chart(style_fig(fig, "Promotion Effect on Demand"), use_container_width=True)

with col2:
    st.subheader("Demand vs Epidemic")
    fig = px.box(df, x="Epidemic", y="Demand",
                 labels={"Epidemic": "Epidemic (0=No, 1=Yes)"})
    st.plotly_chart(style_fig(fig, "Epidemic Effect on Demand"), use_container_width=True)

st.subheader("Average Demand by Discount Level")
disc = df.groupby("Discount")["Demand"].mean().reset_index()
fig = px.line(disc, x="Discount", y="Demand", markers=True)
st.plotly_chart(style_fig(fig, "Demand vs Discount %"), use_container_width=True)
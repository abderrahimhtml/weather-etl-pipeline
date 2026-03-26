import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Clima España",
    page_icon="🌤️",
    layout="wide"
)

@st.cache_data
def load_data():
    engine = create_engine("sqlite:///data/weather.db")
    df = pd.read_sql("SELECT * FROM weather_data", engine)
    return df

df = load_data()

st.title("Dashboard Clima España")
st.markdown("Pipeline ETL en tiempo real — datos extraídos con Python y OpenWeatherMap")

# Separador
st.divider()

# KPIs — fila superior
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Temp. Máxima", f"{df['temperatura'].max():.1f} °C")
with col2:
    st.metric("Temp. Mínima", f"{df['temperatura'].min():.1f} °C")
with col3:
    st.metric("Humedad Media", f"{df['humedad'].mean():.0f} %")
with col4:
    st.metric("Viento Medio", f"{df['velocidad_viento'].mean():.1f} m/s")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperatura por ciudad")
    fig_temp = px.bar(
        df.groupby("ciudad")["temperatura"].mean().reset_index(),
        x="ciudad",
        y="temperatura",
        color="temperatura",
        color_continuous_scale="RdYlBu_r",
        labels={"temperatura": "Temperatura (°C)", "ciudad": "Ciudad"}
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("Humedad por ciudad")
    fig_hum = px.bar(
        df.groupby("ciudad")["humedad"].mean().reset_index(),
        x="ciudad",
        y="humedad",
        color="humedad",
        color_continuous_scale="Blues",
        labels={"humedad": "Humedad (%)", "ciudad": "Ciudad"}
    )
    st.plotly_chart(fig_hum, use_container_width=True)

st.subheader("Velocidad del viento por ciudad")
fig_viento = px.bar(
    df.groupby("ciudad")["velocidad_viento"].mean().reset_index(),
    x="ciudad",
    y="velocidad_viento",
    color="velocidad_viento",
    color_continuous_scale="Greens",
    labels={"velocidad_viento": "Viento (m/s)", "ciudad": "Ciudad"}
)
st.plotly_chart(fig_viento, use_container_width=True)

st.divider()

st.subheader("Datos completos")
st.dataframe(
    df[["ciudad", "temperatura", "sensacion_termica", 
        "humedad", "descripcion", "velocidad_viento", "fecha_extraccion"]],
    use_container_width=True
)
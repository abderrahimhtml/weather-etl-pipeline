from __future__ import annotations

from pathlib import Path
import unicodedata

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Global Weather Dashboard",
    layout="wide",
)

DB_PATH = Path("data/weather.db")
DUCKDB_PATH = Path("data/weather_warehouse.duckdb")
TABLE_NAME = "weather_data"
REQUIRED_COLUMNS = [
    "ciudad", "temperatura", "sensacion_termica",
    "humedad", "descripcion", "velocidad_viento", "fecha_extraccion",
]

CITY_COORDS = {
    "Madrid": (40.4168, -3.7038),
    "Barcelona": (41.3874, 2.1686),
    "Valencia": (39.4699, -0.3763),
    "Sevilla": (37.3891, -5.9845),
    "Bilbao": (43.2630, -2.9350),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Rome": (41.9028, 12.4964),
    "Tokyo": (35.6762, 139.6503),
    "Beijing": (39.9042, 116.4074),
    "Shanghai": (31.2304, 121.4737),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Toronto": (43.6532, -79.3832),
    "Mexico City": (19.4326, -99.1332),
    "São Paulo": (-23.5505, -46.6333),
    "Buenos Aires": (-34.6037, -58.3816),
    "Lima": (-12.0464, -77.0428),
    "Bogotá": (4.7110, -74.0721),
    "Santiago": (-33.4489, -70.6693),
    "Cairo": (30.0444, 31.2357),
    "Lagos": (6.5244, 3.3792),
    "Nairobi": (-1.2921, 36.8219),
    "Johannesburg": (-26.2041, 28.0473),
    "Casablanca": (33.5731, -7.5898),
    "Moscow": (55.7558, 37.6173),
    "Istanbul": (41.0082, 28.9784),
    "Dubai": (25.2048, 55.2708),
    "Riyadh": (24.7136, 46.6753),
    "Tehran": (35.6892, 51.3890),
    "Bangkok": (13.7563, 100.5018),
    "Jakarta": (-6.2088, 106.8456),
    "Singapore": (1.3521, 103.8198),
    "Kuala Lumpur": (3.1390, 101.6869),
    "Manila": (14.5995, 120.9842),
    "Seoul": (37.5665, 126.9780),
    "Sydney": (-33.8688, 151.2093),
    "Melbourne": (-37.8136, 144.9631),
    "Auckland": (-36.8509, 174.7645),
    "Karachi": (24.8607, 67.0011),
    "Dhaka": (23.8103, 90.4125),
    "Colombo": (6.9271, 79.8612),
    "Kathmandu": (27.7172, 85.3240),
    "Islamabad": (33.6844, 73.0479),
    "Kabul": (34.5553, 69.2075),
    "Pekín": (39.9042, 116.4074),
    "Seville": (37.3891, -5.9845),
}


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
    return df


@st.cache_data(show_spinner=False)
def load_warehouse_summary() -> pd.DataFrame:
    if not DUCKDB_PATH.exists():
        return pd.DataFrame()
    conn = duckdb.connect(str(DUCKDB_PATH))
    df = conn.execute("SELECT * FROM avg_temperature").df()
    conn.close()
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    data = df.copy()
    data.columns = [
        unicodedata.normalize("NFKD", str(c)).encode("ascii", "ignore").decode("ascii").strip().lower()
        for c in data.columns
    ]
    rename_map = {
        "sensacion termica": "sensacion_termica",
        "sensaciontermica": "sensacion_termica",
        "velocidad viento": "velocidad_viento",
        "fecha extraccion": "fecha_extraccion",
    }
    data = data.rename(columns=rename_map)
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    data["temperatura"] = pd.to_numeric(data["temperatura"], errors="coerce")
    data["sensacion_termica"] = pd.to_numeric(data["sensacion_termica"], errors="coerce")
    data["humedad"] = pd.to_numeric(data["humedad"], errors="coerce")
    data["velocidad_viento"] = pd.to_numeric(data["velocidad_viento"], errors="coerce")
    data["fecha_extraccion"] = pd.to_datetime(data["fecha_extraccion"], errors="coerce")
    data = data.dropna(subset=["ciudad", "fecha_extraccion"])
    return data


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    st.sidebar.header("Filtros")
    cities = sorted(df["ciudad"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect("Ciudades", options=cities, default=cities)
    min_date = df["fecha_extraccion"].min().date()
    max_date = df["fecha_extraccion"].max().date()
    date_range = st.sidebar.date_input(
        "Rango de fechas", value=(min_date, max_date),
        min_value=min_date, max_value=max_date,
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
    filtered = df[
        (df["ciudad"].isin(selected_cities))
        & (df["fecha_extraccion"].dt.date >= start_date)
        & (df["fecha_extraccion"].dt.date <= end_date)
    ]
    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperatura máxima", f"{df['temperatura'].max():.1f} °C")
    c2.metric("Temperatura mínima", f"{df['temperatura'].min():.1f} °C")
    c3.metric("Humedad media", f"{df['humedad'].mean():.0f} %")
    c4.metric("Viento medio", f"{df['velocidad_viento'].mean():.1f} m/s")


def render_charts(df: pd.DataFrame) -> None:
    st.subheader("Resumen por ciudad")
    summary = (
        df.groupby("ciudad", as_index=False)
        .agg(
            temperatura_media=("temperatura", "mean"),
            humedad_media=("humedad", "mean"),
            viento_medio=("velocidad_viento", "mean"),
        )
        .sort_values("temperatura_media", ascending=False)
    )

    left, right = st.columns(2)
    with left:
        fig_temp = px.bar(
            summary, x="ciudad", y="temperatura_media",
            color="temperatura_media", color_continuous_scale="RdYlBu_r",
            labels={"ciudad": "Ciudad", "temperatura_media": "Temperatura media (°C)"},
            template="plotly_white",
        )
        fig_temp.update_layout(margin=dict(l=10, r=10, t=20, b=80),
                               coloraxis_showscale=False,
                               xaxis_tickangle=-45)
        st.plotly_chart(fig_temp, use_container_width=True)

    with right:
        fig_hum = px.bar(
            summary, x="ciudad", y="humedad_media",
            color="humedad_media", color_continuous_scale="Blues",
            labels={"ciudad": "Ciudad", "humedad_media": "Humedad media (%)"},
            template="plotly_white",
        )
        fig_hum.update_layout(margin=dict(l=10, r=10, t=20, b=80),
                              coloraxis_showscale=False,
                              xaxis_tickangle=-45)
        st.plotly_chart(fig_hum, use_container_width=True)

    st.subheader("Mapa meteorológico global")
    map_df = summary.copy()
    map_df["lat"] = map_df["ciudad"].map(lambda x: CITY_COORDS.get(x, (None, None))[0])
    map_df["lon"] = map_df["ciudad"].map(lambda x: CITY_COORDS.get(x, (None, None))[1])
    map_df = map_df.dropna(subset=["lat", "lon"])

    if map_df.empty:
        st.info("No hay coordenadas disponibles para las ciudades seleccionadas.")
    else:
        fig_map = px.scatter_map(
            map_df, lat="lat", lon="lon",
           size=map_df["temperatura_media"].clip(lower=1), size_max=20, color="temperatura_media",
            hover_name="ciudad",
            hover_data={
    "temperatura_media": ":.1f",
    "humedad_media": ":.0f",
    "lat": False,
    "lon": False,
},
            color_continuous_scale="RdYlBu_r",
            zoom=1.5,
            center={"lat": 20, "lon": 10},
            map_style="open-street-map",
            labels={"temperatura_media": "Temperatura (°C)"},
            template="plotly_white",
        )
        fig_map.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_map, use_container_width=True)


def render_warehouse(df: pd.DataFrame) -> None:
    if df.empty:
        return
    st.subheader("Data Warehouse — Top 10 ciudades por temperatura (DuckDB)")
    top10 = df.head(10)
    cols = st.columns(5)
    for i, row in top10.iterrows():
        with cols[i % 5]:
            st.metric(
                label=row["ciudad"],
                value=f"{row['temp_media']} °C",
                delta=f"Sensación {row['sensacion_media']} °C"
            )
    st.dataframe(df, use_container_width=True)


def main() -> None:
    st.title("Global Weather Dashboard")
    st.markdown("Datos meteorológicos en tiempo real de las 50 ciudades más importantes del mundo.")

    raw_df = load_data()
    df = prepare_data(raw_df)

    if df.empty:
        st.warning("No se encontraron datos.")
        return

    filtered = filter_data(df)
    if filtered.empty:
        st.warning("Los filtros actuales no devuelven resultados.")
        return

    st.divider()
    render_kpis(filtered)
    st.divider()
    render_charts(filtered)
    st.divider()
    warehouse_df = load_warehouse_summary()
    render_warehouse(warehouse_df)
    st.divider()

    st.subheader("Detalle de datos")
    visible_columns = [c for c in REQUIRED_COLUMNS if c in filtered.columns]
    st.dataframe(
        filtered[visible_columns].sort_values("fecha_extraccion", ascending=False),
        use_container_width=True,
        height=350,
    )


if __name__ == "__main__":
    main()
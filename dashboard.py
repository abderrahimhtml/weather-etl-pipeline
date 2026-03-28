from __future__ import annotations

from pathlib import Path
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
import duckdb

st.set_page_config(
    page_title="Panel Profesional de Clima en España",
    layout="wide",
)


DB_PATH = Path("data/weather.db")
TABLE_NAME = "weather_data"
REQUIRED_COLUMNS = [
    "ciudad",
    "temperatura",
    "sensacion_termica",
    "humedad",
    "descripcion",
    "velocidad_viento",
    "fecha_extraccion",
]

CITY_COORDS = {
    "Madrid": (40.4168, -3.7038),
    "Barcelona": (41.3874, 2.1686),
    "Valencia": (39.4699, -0.3763),
    "Sevilla": (37.3891, -5.9845),
    "Málaga": (36.7213, -4.4214),
    "Bilbao": (43.2630, -2.9350),
    "Zaragoza": (41.6488, -0.8891),
    "Murcia": (37.9922, -1.1307),
    "Palma": (39.5696, 2.6502),
    "Valladolid": (41.6523, -4.7245),
}


DUCKDB_PATH = Path("data/weather_warehouse.duckdb")

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


def corporate_style() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 1.4rem;
                max-width: 1400px;
            }
            h1, h2, h3 {
                letter-spacing: 0.2px;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.65rem;
            }
            .caption {
                color: #4b5563;
                font-size: 0.95rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    st.sidebar.header("Filtros")

    cities = sorted(df["ciudad"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "Ciudades",
        options=cities,
        default=cities,
    )

    min_date = df["fecha_extraccion"].min().date()
    max_date = df["fecha_extraccion"].max().date()
    date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
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
            summary,
            x="ciudad",
            y="temperatura_media",
            color="temperatura_media",
            color_continuous_scale="RdYlBu_r",
            labels={"ciudad": "Ciudad", "temperatura_media": "Temperatura media (°C)"},
            template="plotly_white",
        )
        fig_temp.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig_temp, use_container_width=True)

    with right:
        fig_hum = px.bar(
            summary,
            x="ciudad",
            y="humedad_media",
            color="humedad_media",
            color_continuous_scale="Blues",
            labels={"ciudad": "Ciudad", "humedad_media": "Humedad media (%)"},
            template="plotly_white",
        )
        fig_hum.update_layout(margin=dict(l=10, r=10, t=20, b=10), coloraxis_showscale=False)
        st.plotly_chart(fig_hum, use_container_width=True)

    st.subheader("Evolución temporal")
    evolution = (
        df.set_index("fecha_extraccion")
        .resample("D")
        .agg(temperatura_media=("temperatura", "mean"), humedad_media=("humedad", "mean"))
        .dropna()
        .reset_index()
    )
    fig_evolution = px.line(
        evolution,
        x="fecha_extraccion",
        y=["temperatura_media", "humedad_media"],
        labels={"value": "Valor", "fecha_extraccion": "Fecha", "variable": "Métrica"},
        template="plotly_white",
    )
    fig_evolution.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig_evolution, use_container_width=True)

    st.subheader("Mapa meteorológico (visual realista)")
    map_df = summary.copy()
    map_df["lat"] = map_df["ciudad"].map(lambda x: CITY_COORDS.get(x, (None, None))[0])
    map_df["lon"] = map_df["ciudad"].map(lambda x: CITY_COORDS.get(x, (None, None))[1])
    map_df = map_df.dropna(subset=["lat", "lon"])

    if map_df.empty:
        st.info("No hay coordenadas disponibles para las ciudades seleccionadas.")
    else:
        fig_map = px.scatter_map(
            map_df,
            lat="lat",
            lon="lon",
            size="temperatura_media",
            color="humedad_media",
            hover_name="ciudad",
            color_continuous_scale="Viridis",
            zoom=4.5,
            center={"lat": 40.2, "lon": -3.5},
            map_style="open-street-map",
            labels={"humedad_media": "Humedad media (%)"},
            template="plotly_white",
        )
        fig_map.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_map, use_container_width=True)
def render_warehouse(df: pd.DataFrame) -> None:
    if df.empty:
        return
    st.subheader("Data Warehouse — Resumen analítico (DuckDB)")
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            st.metric(row["ciudad"], f"{row['temp_media']} °C", f"Sensación {row['sensacion_media']} °C")
    st.dataframe(df, use_container_width=True)

def main() -> None:
    corporate_style()

    st.title("Panel Profesional de Clima en España")
    st.markdown(
        '<p class="caption">Información operativa para análisis meteorológico, con visualización corporativa y filtros de negocio.</p>',
        unsafe_allow_html=True,
    )

    raw_df = load_data()
    df = prepare_data(raw_df)

    if df.empty:
        st.warning("No se encontraron datos en la base SQLite (`data/weather.db`).")
        return

    filtered = filter_data(df)
    if filtered.empty:
        st.warning("Los filtros actuales no devuelven resultados.")
        return

    st.divider()
    render_kpis(filtered)
    st.divider()
    render_charts(filtered)
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

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Gestión de Citas Médicas",
    page_icon="🏥",
    layout="wide"
)

# Cargar datos
df = pd.read_csv("citas_medicas.csv")
df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.month

# Título
st.title("🏥 Dashboard de Gestión de Citas Médicas")
st.markdown(
    "### Plataforma de Inteligencia de Negocios para el análisis de citas médicas"
)
st.markdown("---")

# Indicadores (KPIs)
total = len(df)
atendidas = (df["estado"] == "Atendida").sum()
canceladas = (df["estado"] == "Cancelada").sum()
no_asistio = (df["estado"] == "No asistió").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📋 Total de Citas", total)
col2.metric("✅ Atendidas", atendidas)
col3.metric("❌ Canceladas", canceladas)
col4.metric("⚠️ No Asistió", no_asistio)

st.markdown("---")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Citas por Especialidad")

    esp = (
        df["especialidad"]
        .value_counts()
        .reset_index()
    )

    esp.columns = ["Especialidad", "Cantidad"]

    fig1 = px.bar(
        esp,
        x="Especialidad",
        y="Cantidad",
        color="Cantidad",
        color_continuous_scale="Blues",
        text="Cantidad"
    )

    fig1.update_layout(showlegend=False)

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🥧 Estado de las Citas")

    fig2 = px.pie(
        df,
        names="estado",
        hole=0.45,
        color="estado",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig2, use_container_width=True)

# Línea temporal
st.subheader("📈 Evolución Mensual de las Citas")
mes = df.groupby("mes").size().reset_index(name="Cantidad")

fig3 = px.line(
    mes,
    x="mes",
    y="Cantidad",
    markers=True,
    line_shape="spline"
)

fig3.update_traces(line_color="#0A84FF", line_width=4)
st.plotly_chart(fig3, use_container_width=True)

# Tabla
st.subheader("📄 Vista previa del Dataset")
st.dataframe(df, use_container_width=True)


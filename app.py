import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Demo para RAMÓN HC de Streamlit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
    }
    .feature-badge {
        display: inline-block;
        background: #f3f4f6;
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        color: #374151;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=60)
    st.markdown("## 🗂️ Navegación")
    
    seccion = st.radio(
        "Elige una sección:",
        ["🏠 Inicio", "📊 Dashboard", "🤖 IA / Predicción", "🗂️ Datos", "🎨 Widgets"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### ⚙️ Configuración global")
    tema = st.selectbox("Paleta de colores", ["Morado", "Azul", "Verde", "Naranja"])
    mostrar_raw = st.toggle("Mostrar datos en crudo", value=False)
    
    color_map = {"Morado": "plasma", "Azul": "blues", "Verde": "greens", "Naranja": "oranges"}
    colorscale = color_map[tema]
    
    st.divider()
    st.caption("Hecho usando Streamlit 💪")

# ── Datos de ejemplo ─────────────────────────────────────────────────────────
@st.cache_data
def generar_datos_ventas():
    np.random.seed(42)
    fechas = pd.date_range(start="2024-01-01", periods=365, freq="D")
    categorias = ["Electrónica", "Ropa", "Hogar", "Alimentación", "Deportes"]
    
    rows = []
    for fecha in fechas:
        for cat in categorias:
            base = {"Electrónica": 5000, "Ropa": 3000, "Hogar": 2000,
                    "Alimentación": 4000, "Deportes": 1500}[cat]
            trend = (fecha - fechas[0]).days * 2
            seasonal = np.sin((fecha.dayofyear / 365) * 2 * np.pi) * base * 0.3
            noise = np.random.normal(0, base * 0.1)
            ventas = max(0, base + trend + seasonal + noise)
            rows.append({"Fecha": fecha, "Categoría": cat,
                         "Ventas": round(ventas), "Unidades": int(ventas / 50)})
    return pd.DataFrame(rows)

df = generar_datos_ventas()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN: INICIO
# ════════════════════════════════════════════════════════════════════════════
if seccion == "🏠 Inicio":
    st.markdown('<h1 class="main-title">🚀 Demo App — Streamlit</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Una demostración interactiva de todo lo que puedes construir</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ventas Totales", "€ 2.4M", "+12.5%", delta_color="normal")
    with col2:
        st.metric("Usuarios Activos", "8,342", "+342 hoy")
    with col3:
        st.metric("Tasa Conversión", "4.7%", "-0.3%", delta_color="inverse")
    with col4:
        st.metric("NPS Score", "72", "+8 pts")
    
    st.divider()
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📈 Evolución de ventas (últimos 90 días)")
        df_90 = df[df["Fecha"] >= df["Fecha"].max() - timedelta(days=90)]
        df_agg = df_90.groupby("Fecha")["Ventas"].sum().reset_index()
        fig = px.area(df_agg, x="Fecha", y="Ventas",
                      color_discrete_sequence=["#6366f1"],
                      template="plotly_white")
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("🥧 Cuota por categoría")
        df_cat = df.groupby("Categoría")["Ventas"].sum().reset_index()
        fig2 = px.pie(df_cat, names="Categoría", values="Ventas",
                      color_discrete_sequence=px.colors.sequential.Plasma_r,
                      hole=0.4)
        fig2.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=300,
                           showlegend=True, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    st.subheader("✨ ¿Qué puedes hacer con Streamlit?")
    features = [
        "📊 Dashboards interactivos", "🤖 Apps de Machine Learning",
        "📁 Carga y procesado de ficheros", "🗺️ Mapas y geolocalización",
        "💬 Chatbots con IA", "📡 Conexión a bases de datos",
        "🔐 Autenticación de usuarios", "🌐 Deploy en la nube gratis",
        "🎨 Temas personalizados", "⚡ Actualizaciones en tiempo real"
    ]
    badges_html = "".join([f'<span class="feature-badge">{f}</span>' for f in features])
    st.markdown(badges_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif seccion == "📊 Dashboard":
    st.title("📊 Dashboard de Ventas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cat_sel = st.multiselect("Categorías", df["Categoría"].unique(),
                                  default=list(df["Categoría"].unique()))
    with col2:
        fecha_ini = st.date_input("Desde", value=datetime(2024, 1, 1))
    with col3:
        fecha_fin = st.date_input("Hasta", value=datetime(2024, 12, 31))
    
    mask = (
        df["Categoría"].isin(cat_sel) &
        (df["Fecha"].dt.date >= fecha_ini) &
        (df["Fecha"].dt.date <= fecha_fin)
    )
    df_fil = df[mask]
    
    if df_fil.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ventas por categoría y mes")
            df_mensual = df_fil.copy()
            df_mensual["Mes"] = df_mensual["Fecha"].dt.to_period("M").astype(str)
            df_m = df_mensual.groupby(["Mes", "Categoría"])["Ventas"].sum().reset_index()
            fig = px.bar(df_m, x="Mes", y="Ventas", color="Categoría",
                         barmode="stack", template="plotly_white",
                         color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=0),
                              xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Mapa de calor — día de semana × categoría")
            df_fil2 = df_fil.copy()
            df_fil2["DíaSemana"] = df_fil2["Fecha"].dt.day_name()
            dias_orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            pivot = df_fil2.groupby(["DíaSemana", "Categoría"])["Ventas"].mean().unstack()
            pivot = pivot.reindex(dias_orden)
            fig3 = px.imshow(pivot, color_continuous_scale=colorscale,
                             labels=dict(color="Ventas (€)"), template="plotly_white",
                             aspect="auto")
            fig3.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("🏆 Top 10 días con más ventas")
        top10 = df_fil.groupby("Fecha")["Ventas"].sum().nlargest(10).reset_index()
        top10["Fecha"] = top10["Fecha"].dt.strftime("%d %b %Y")
        top10["Ventas"] = top10["Ventas"].apply(lambda x: f"€ {x:,.0f}")
        st.dataframe(top10, use_container_width=True, hide_index=True)
        
        if mostrar_raw:
            st.subheader("Datos en crudo")
            st.dataframe(df_fil.head(200), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN: IA / PREDICCIÓN
# ════════════════════════════════════════════════════════════════════════════
elif seccion == "🤖 IA / Predicción":
    st.title("🤖 Predicción con IA")
    st.info("Ejemplo de cómo integrar modelos de ML en Streamlit. Aquí usamos una regresión polinómica simple para ilustrar el flujo.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Parámetros del modelo")
        categoria = st.selectbox("Categoría a predecir", df["Categoría"].unique())
        dias_pred = st.slider("Días a predecir", 7, 90, 30)
        grado = st.slider("Grado polinómico", 1, 5, 2)
        
        if st.button("🚀 Entrenar y predecir", type="primary", use_container_width=True):
            with st.spinner("Entrenando modelo..."):
                time.sleep(1.2)
            st.session_state["pred_ready"] = True
            st.session_state["pred_cat"] = categoria
            st.session_state["pred_dias"] = dias_pred
            st.session_state["pred_grado"] = grado
            st.success("¡Modelo entrenado!")
        
        if st.session_state.get("pred_ready"):
            st.markdown("---")
            st.markdown("**Métricas del modelo:**")
            r2 = np.random.uniform(0.82, 0.97)
            rmse = np.random.uniform(200, 600)
            st.metric("R² Score", f"{r2:.4f}")
            st.metric("RMSE", f"€ {rmse:.0f}")
    
    with col2:
        st.subheader("📈 Histórico + Predicción")
        
        if st.session_state.get("pred_ready"):
            cat = st.session_state["pred_cat"]
            dias = st.session_state["pred_dias"]
            
            df_cat = df[df["Categoría"] == cat].groupby("Fecha")["Ventas"].sum().reset_index()
            df_cat = df_cat.tail(120)
            
            last_date = df_cat["Fecha"].max()
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=dias)
            
            x = np.arange(len(df_cat))
            y = df_cat["Ventas"].values
            coeffs = np.polyfit(x, y, st.session_state["pred_grado"])
            poly = np.poly1d(coeffs)
            
            x_fut = np.arange(len(df_cat), len(df_cat) + dias)
            y_pred = poly(x_fut) + np.random.normal(0, 300, dias)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_cat["Fecha"], y=df_cat["Ventas"],
                                     name="Histórico", line=dict(color="#6366f1", width=2)))
            fig.add_trace(go.Scatter(x=future_dates, y=y_pred,
                                     name="Predicción", line=dict(color="#ec4899", width=2, dash="dash"),
                                     fill="tozeroy", fillcolor="rgba(236,72,153,0.1)"))
            fig.update_layout(template="plotly_white", height=420,
                              margin=dict(l=0, r=0, t=20, b=0),
                              legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style='height:400px; display:flex; align-items:center; justify-content:center;
                        background:#f9fafb; border-radius:12px; border: 2px dashed #d1d5db;'>
                <div style='text-align:center; color:#9ca3af;'>
                    <div style='font-size:3rem'>🤖</div>
                    <div style='font-size:1.1rem; margin-top:0.5rem'>Configura y entrena el modelo</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN: DATOS
# ════════════════════════════════════════════════════════════════════════════
elif seccion == "🗂️ Datos":
    st.title("🗂️ Gestión de Datos")
    
    tab1, tab2, tab3 = st.tabs(["📤 Subir fichero", "🔍 Explorar datos", "💾 Descargar"])
    
    with tab1:
        st.subheader("Sube tu propio CSV")
        uploaded = st.file_uploader("Arrastra o selecciona un fichero CSV", type=["csv", "xlsx"])
        
        if uploaded:
            if uploaded.name.endswith(".csv"):
                df_up = pd.read_csv(uploaded)
            else:
                df_up = pd.read_excel(uploaded)
            
            st.success(f"✅ Fichero cargado: **{uploaded.name}** — {len(df_up):,} filas × {len(df_up.columns)} columnas")
            st.dataframe(df_up.head(50), use_container_width=True)
            
            st.subheader("Estadísticas básicas")
            st.dataframe(df_up.describe(), use_container_width=True)
        else:
            st.info("👆 Sube un fichero para verlo aquí. Mientras tanto, exploramos los datos de ejemplo en la pestaña **Explorar datos**.")
    
    with tab2:
        st.subheader("Explorador interactivo")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            col_x = st.selectbox("Eje X", ["Fecha", "Categoría", "Ventas", "Unidades"])
        with col2:
            col_y = st.selectbox("Eje Y", ["Ventas", "Unidades"], index=0)
        with col3:
            tipo = st.selectbox("Tipo de gráfico", ["Líneas", "Barras", "Dispersión", "Boxplot"])
        
        df_agg2 = df.groupby(["Fecha", "Categoría"])[["Ventas", "Unidades"]].sum().reset_index()
        
        if tipo == "Líneas":
            fig = px.line(df_agg2, x="Fecha", y=col_y, color="Categoría",
                          template="plotly_white", color_discrete_sequence=px.colors.qualitative.Vivid)
        elif tipo == "Barras":
            df_cat = df.groupby("Categoría")[[col_y]].sum().reset_index()
            fig = px.bar(df_cat, x="Categoría", y=col_y, color="Categoría",
                         template="plotly_white", color_discrete_sequence=px.colors.qualitative.Vivid)
        elif tipo == "Dispersión":
            fig = px.scatter(df.sample(500), x="Ventas", y="Unidades", color="Categoría",
                             template="plotly_white", color_discrete_sequence=px.colors.qualitative.Vivid)
        else:
            fig = px.box(df, x="Categoría", y=col_y, color="Categoría",
                         template="plotly_white", color_discrete_sequence=px.colors.qualitative.Vivid)
        
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Descargar datos procesados")
        
        df_export = df.groupby(["Fecha", "Categoría"])[["Ventas", "Unidades"]].sum().reset_index()
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv_data,
                file_name="ventas_demo.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col2:
            st.info("También puedes descargar como Excel conectando con la librería `openpyxl`.")

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN: WIDGETS
# ════════════════════════════════════════════════════════════════════════════
elif seccion == "🎨 Widgets":
    st.title("🎨 Galería de Widgets")
    st.caption("Todos los componentes interactivos que Streamlit ofrece de serie")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Inputs de texto")
        nombre = st.text_input("Tu nombre", placeholder="Escribe aquí...")
        bio = st.text_area("Descripción corta", height=80, placeholder="Cuéntanos algo...")
        password = st.text_input("Contraseña", type="password")
        if nombre:
            st.markdown(f"👋 ¡Hola, **{nombre}**!")
        
        st.subheader("🔢 Numéricos y rangos")
        edad = st.number_input("Edad", min_value=0, max_value=120, value=25)
        rango = st.slider("Rango de precios (€)", 0, 1000, (100, 500))
        st.caption(f"Seleccionado: {rango[0]}€ — {rango[1]}€")
        prog = st.slider("Progreso manual", 0, 100, 60)
        st.progress(prog / 100)
    
    with col2:
        st.subheader("✅ Selecciones")
        opcion = st.radio("Método de pago", ["Tarjeta", "Transferencia", "PayPal", "Bizum"])
        multi = st.multiselect("Categorías favoritas", df["Categoría"].unique(), default=["Electrónica"])
        activo = st.checkbox("Recibir notificaciones", value=True)
        toggle = st.toggle("Modo oscuro (simulado)", value=False)
        select = st.selectbox("País", ["España", "México", "Argentina", "Colombia", "Chile"])
        
        st.subheader("📅 Fecha y hora")
        fecha = st.date_input("Fecha de inicio")
        hora = st.time_input("Hora")
        st.caption(f"Seleccionado: {fecha} a las {hora}")
    
    st.divider()
    st.subheader("🎭 Feedback y estado")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        if st.button("✅ Éxito", use_container_width=True):
            st.success("¡Operación completada con éxito!")
    with col4:
        if st.button("⚠️ Advertencia", use_container_width=True):
            st.warning("Esto es una advertencia.")
    with col5:
        if st.button("❌ Error", use_container_width=True):
            st.error("Algo salió mal.")
    
    st.divider()
    st.subheader("⏳ Progreso y spinners")
    if st.button("Simular proceso largo", type="primary"):
        bar = st.progress(0, text="Iniciando...")
        for i in range(101):
            time.sleep(0.02)
            bar.progress(i / 100, text=f"Procesando... {i}%")
        st.balloons()
        st.success("¡Proceso completado!")

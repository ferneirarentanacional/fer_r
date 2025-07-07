# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 10:39:53 2025

@author: fneira
"""

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random
import io

# Configuración de página
st.set_page_config(page_title="SGI Mobile", page_icon="📱", layout="centered", initial_sidebar_state="collapsed")

# CSS móvil
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    header {visibility: hidden;}
    
    .main .block-container {
        padding: 0rem 1rem;
        max-width: 420px;
        margin: 0 auto;
    }
    
    .mobile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .mobile-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #f0f0f0;
    }
    
    .mobile-metric {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }
    
    .mobile-list-item {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .status-active { background: #d4edda; color: #155724; }
    .status-pending { background: #fff3cd; color: #856404; }
    .status-closed { background: #f8d7da; color: #721c24; }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stSelectbox select {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Función para generar datos
@st.cache_data
def generate_data():
    # Pólizas
    polizas = []
    for i in range(25):
        poliza = {
            "id": f"POL-{1000 + i}",
            "cliente": f"Cliente {chr(65 + i % 26)}{i // 26 + 1}",
            "rut_cliente": f"{random.randint(10000000, 19999999)}-{random.randint(0, 9)}",
            "tipo": random.choice(["🚗 Auto", "🏠 Hogar", "🏢 Empresarial"]),
            "estado": random.choice(["Activa", "Pendiente", "Vencida"]),
            "prima": random.randint(50000, 500000),
            "vencimiento": (datetime.now() + timedelta(days=random.randint(1, 365))).strftime("%d/%m/%Y"),
            "cuotas_pendientes": random.randint(0, 8)
        }
        polizas.append(poliza)
    
    # Siniestros
    siniestros = []
    liquidadores = ["Liquidador A", "Liquidador B", "Liquidador C", "Liquidador D"]
    for i in range(30):
        siniestro = {
            "id": f"SIN-{2000 + i}",
            "tipo": random.choice(["🚗 Choque", "🔥 Incendio", "💧 Daños", "🚨 Robo"]),
            "estado": random.choice(["Abierto", "En proceso", "Cerrado"]),
            "monto": random.randint(100000, 2000000),
            "fecha": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%d/%m/%Y"),
            "liquidador": random.choice(liquidadores),
            "cliente": f"Cliente {chr(65 + random.randint(0, 25))}{random.randint(1, 3)}",
            "rut_cliente": f"{random.randint(10000000, 19999999)}-{random.randint(0, 9)}"
        }
        siniestros.append(siniestro)
    
    # Siniestralidad anual
    siniestralidad = {
        "año": ["2024", "2025"],
        "vehiculos_siniestros": [45000000, 38000000],
        "vehiculos_prima": [180000000, 195000000],
        "property_siniestros": [28000000, 32000000],
        "property_prima": [120000000, 130000000]
    }
    
    return pd.DataFrame(polizas), pd.DataFrame(siniestros), siniestralidad

# Función para Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    return output.getvalue()

# Inicializar datos
df_polizas, df_siniestros, siniestralidad = generate_data()

# Estado de navegación
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

# Header
st.markdown("""
<div class="mobile-header">
    <h2>📱 SGI Mobile</h2>
    <p>Bienvenido, Corredor SGI</p>
</div>
""", unsafe_allow_html=True)

# Filtro RUT Global
st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
st.subheader("🔍 Filtro Global")
filtro_rut = st.text_input("RUT Cliente:", placeholder="12345678-9")
st.markdown('</div>', unsafe_allow_html=True)

# Navegación
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠\nInicio", key="nav_home"):
        st.session_state.current_page = 'dashboard'
with col2:
    if st.button("📋\nPólizas", key="nav_policies"):
        st.session_state.current_page = 'polizas'
with col3:
    if st.button("⚠️\nSiniestros", key="nav_claims"):
        st.session_state.current_page = 'siniestros'
with col4:
    if st.button("📊\nSiniestralidad", key="nav_claims_stats"):
        st.session_state.current_page = 'siniestralidad'
with col5:
    if st.button("💳\nCuotas", key="nav_installments"):
        st.session_state.current_page = 'cuotas'
with col6:
    if st.button("🤖\nAsistente", key="nav_assistant"):
        st.session_state.current_page = 'asistente'

# Dashboard
if st.session_state.current_page == 'dashboard':
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="mobile-metric">
            <p class="metric-value">24</p>
            <p class="metric-label">Pólizas Activas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="mobile-metric">
            <p class="metric-value">8</p>
            <p class="metric-label">Siniestros Pendientes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("⚡ Acciones Rápidas")
    
    if st.button("🔍 Consultar Póliza", key="quick_search"):
        st.session_state.current_page = 'polizas'
        st.rerun()
    
    if st.button("📞 Contactar Asistencia", key="quick_help"):
        st.info("📞 Llamando a línea de asistencia: +56 2 2345 6789")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Pólizas
elif st.session_state.current_page == 'polizas':
    df_filtered = df_polizas.copy()
    if filtro_rut:
        df_filtered = df_filtered[df_filtered['rut_cliente'].str.contains(filtro_rut, case=False, na=False)]
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    search_term = st.text_input("🔍 Buscar póliza...", placeholder="Número de póliza o cliente")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    filtro_tipo = st.selectbox("Filtrar por tipo:", ["Todos"] + list(df_polizas['tipo'].unique()))
    filtro_estado = st.selectbox("Filtrar por estado:", ["Todos"] + list(df_polizas['estado'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if filtro_tipo != "Todos":
        df_filtered = df_filtered[df_filtered['tipo'] == filtro_tipo]
    if filtro_estado != "Todos":
        df_filtered = df_filtered[df_filtered['estado'] == filtro_estado]
    if search_term:
        df_filtered = df_filtered[
            df_filtered['id'].str.contains(search_term, case=False) |
            df_filtered['cliente'].str.contains(search_term, case=False)
        ]
    
    if not df_filtered.empty:
        excel_data = to_excel(df_filtered)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f"polizas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.subheader(f"📋 Pólizas ({len(df_filtered)})")
    
    for _, poliza in df_filtered.head(10).iterrows():
        estado_class = "status-active" if poliza['estado'] == 'Activa' else "status-pending" if poliza['estado'] == 'Pendiente' else "status-closed"
        
        with st.expander(f"{poliza['tipo']} - {poliza['id']}", expanded=False):
            st.write(f"**Cliente:** {poliza['cliente']}")
            st.write(f"**RUT:** {poliza['rut_cliente']}")
            st.write(f"**Prima:** ${poliza['prima']:,}")
            st.write(f"**Vencimiento:** {poliza['vencimiento']}")
            st.write(f"**Cuotas Pendientes:** {poliza['cuotas_pendientes']}")
            st.markdown(f'<span class="status-badge {estado_class}">{poliza["estado"]}</span>', unsafe_allow_html=True)
            
            if st.button("📄 Ver Detalles", key=f"details_{poliza['id']}"):
                st.info("Cargando detalles de la póliza...")

# Siniestros
elif st.session_state.current_page == 'siniestros':
    df_sin_filtered = df_siniestros.copy()
    if filtro_rut:
        df_sin_filtered = df_sin_filtered[df_sin_filtered['rut_cliente'].str.contains(filtro_rut, case=False, na=False)]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        abiertos = len(df_sin_filtered[df_sin_filtered['estado'] == 'Abierto'])
        st.markdown(f"""
        <div class="mobile-metric" style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa8a8 100%);">
            <p class="metric-value">{abiertos}</p>
            <p class="metric-label">Abiertos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        proceso = len(df_sin_filtered[df_sin_filtered['estado'] == 'En proceso'])
        st.markdown(f"""
        <div class="mobile-metric" style="background: linear-gradient(135deg, #ffd93d 0%, #ffed4a 100%);">
            <p class="metric-value">{proceso}</p>
            <p class="metric-label">En Proceso</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cerrados = len(df_sin_filtered[df_sin_filtered['estado'] == 'Cerrado'])
        st.markdown(f"""
        <div class="mobile-metric" style="background: linear-gradient(135deg, #6bcf7f 0%, #a8e6cf 100%);">
            <p class="metric-value">{cerrados}</p>
            <p class="metric-label">Cerrados</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    filtro_liquidador = st.selectbox("Filtrar por liquidador:", ["Todos"] + list(df_siniestros['liquidador'].unique()))
    if filtro_liquidador != "Todos":
        df_sin_filtered = df_sin_filtered[df_sin_filtered['liquidador'] == filtro_liquidador]
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not df_sin_filtered.empty:
        excel_data = to_excel(df_sin_filtered)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f"siniestros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.subheader(f"📋 Siniestros ({len(df_sin_filtered)})")
    
    for _, siniestro in df_sin_filtered.head(10).iterrows():
        estado_color = "🔴" if siniestro['estado'] == 'Abierto' else "🟡" if siniestro['estado'] == 'En proceso' else "🟢"
        
        with st.expander(f"{siniestro['tipo']} - {siniestro['id']}", expanded=False):
            st.write(f"**Cliente:** {siniestro['cliente']}")
            st.write(f"**RUT:** {siniestro['rut_cliente']}")
            st.write(f"**Fecha:** {siniestro['fecha']}")
            st.write(f"**Monto:** ${siniestro['monto']:,}")
            st.write(f"**Liquidador:** {siniestro['liquidador']}")
            st.write(f"**Estado:** {estado_color} {siniestro['estado']}")

# Siniestralidad
elif st.session_state.current_page == 'siniestralidad':
    st.subheader("📊 Siniestralidad Anual")
    
    # Gráfico comparativo de siniestralidad acumulada
    fig = go.Figure()
    
    # Vehículos
    fig.add_trace(go.Bar(
        name='Vehículos - Siniestros',
        x=siniestralidad["año"],
        y=siniestralidad["vehiculos_siniestros"],
        marker_color='#ff6b6b',
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        name='Vehículos - Prima',
        x=siniestralidad["año"],
        y=siniestralidad["vehiculos_prima"],
        marker_color='#4ecdc4',
        yaxis='y'
    ))
    
    # Property
    fig.add_trace(go.Bar(
        name='Property - Siniestros',
        x=siniestralidad["año"],
        y=siniestralidad["property_siniestros"],
        marker_color='#ff9a9e',
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        name='Property - Prima',
        x=siniestralidad["año"],
        y=siniestralidad["property_prima"],
        marker_color='#a8e6cf',
        yaxis='y'
    ))
    
    fig.update_layout(
        title="Siniestralidad Acumulada por Año",
        barmode='group',
        height=500,
        yaxis_title="Monto ($)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ratios anuales
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("📈 Ratios de Siniestralidad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚗 Vehículos**")
        for i, año in enumerate(siniestralidad["año"]):
            ratio = (siniestralidad["vehiculos_siniestros"][i] / siniestralidad["vehiculos_prima"][i]) * 100
            st.metric(f"{año}", f"{ratio:.1f}%")
    
    with col2:
        st.markdown("**🏠 Property**")
        for i, año in enumerate(siniestralidad["año"]):
            ratio = (siniestralidad["property_siniestros"][i] / siniestralidad["property_prima"][i]) * 100
            st.metric(f"{año}", f"{ratio:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Descarga de datos
    siniestralidad_df = pd.DataFrame({
        'Año': siniestralidad["año"],
        'Vehiculos_Siniestros': siniestralidad["vehiculos_siniestros"],
        'Vehiculos_Prima': siniestralidad["vehiculos_prima"],
        'Property_Siniestros': siniestralidad["property_siniestros"],
        'Property_Prima': siniestralidad["property_prima"]
    })
    
    excel_data = to_excel(siniestralidad_df)
    st.download_button(
        label="📥 Descargar Siniestralidad Excel",
        data=excel_data,
        file_name=f"siniestralidad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Cuotas
elif st.session_state.current_page == 'cuotas':
    df_cuotas = df_polizas[df_polizas['cuotas_pendientes'] > 3].copy()
    
    if filtro_rut:
        df_cuotas = df_cuotas[df_cuotas['rut_cliente'].str.contains(filtro_rut, case=False, na=False)]
    
    st.subheader(f"💳 Pólizas con +3 Cuotas Pendientes ({len(df_cuotas)})")
    
    if df_cuotas.empty:
        st.info("No hay pólizas con más de 3 cuotas pendientes")
    else:
        excel_data = to_excel(df_cuotas)
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f"cuotas_pendientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        for _, poliza in df_cuotas.iterrows():
            color_urgencia = "🔴" if poliza['cuotas_pendientes'] > 6 else "🟡" if poliza['cuotas_pendientes'] > 4 else "🟠"
            
            st.markdown(f"""
            <div class="mobile-list-item">
                <div>
                    <div style="font-weight: bold;">{poliza['tipo']} - {poliza['id']}</div>
                    <div style="font-size: 0.9rem; color: #666;">
                        {poliza['cliente']} • {poliza['rut_cliente']}
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">
                        Prima: ${poliza['prima']:,}
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem;">{color_urgencia}</div>
                    <div style="font-weight: bold; color: #e74c3c;">
                        {poliza['cuotas_pendientes']} cuotas
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Asistente
elif st.session_state.current_page == 'asistente':
    st.subheader("🤖 Asistente SGI SIS")
    
    st.markdown("""
    <div class="mobile-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; 
                        font-size: 2rem; color: white;">🤖</div>
            <h3 style="margin: 0.5rem 0;">Asistente Virtual SGI</h3>
            <p style="color: #666; margin: 0;">Acceso directo a sistemas SGI SIS</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("🔗 Acceso a Sistemas")
    
    sistemas = [
        ("⚠️ Sistema de Siniestros", "https://sgi-sis.com/siniestros"),
        ("💰 Sistema de Primas", "https://sgi-sis.com/primas"),
        ("💳 Sistema de Cuotas", "https://sgi-sis.com/cuotas")
    ]
    
    for nombre, url in sistemas:
        if st.button(f"🌐 {nombre}", key=f"open_{nombre}"):
            st.markdown(f"""
            <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <strong>🔗 Enlace:</strong><br>
                <a href="{url}" target="_blank" style="color: #2e7d32; text-decoration: none;">
                    {url}
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-card">', unsafe_allow_html=True)
    st.subheader("📞 Contacto y Soporte")
    
    st.markdown("**📧 Email:** soporte@sgi-sis.com")
    
    if st.button("💬 Enviar Comentarios", key="send_feedback"):
        comentarios = st.text_area("Escribe tus comentarios:", placeholder="Tu mensaje aquí...")
        if st.button("📤 Enviar", key="submit_feedback"):
            st.success("✅ Comentarios enviados correctamente")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666; font-size: 0.8rem;">
    <p>SGI Mobile App © 2025</p>
    <p>Desarrollado con ❤️ por Renta Impulsa</p>
</div>
""", unsafe_allow_html=True)
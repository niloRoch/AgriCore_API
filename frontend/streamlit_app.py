import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Configuração da página
st.set_page_config(
    page_title="AgroSmart Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API (ajuste conforme necessário)
API_BASE_URL = "http://localhost:8000"

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-info {
        background-color: #d1ecf1;
        border: 1px solid #74b9ff;
        padding: 0.75rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares para chamadas à API
@st.cache_data(ttl=30)
def get_sensors_data():
    try:
        response = requests.get(f"{API_BASE_URL}/sensors/current")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

@st.cache_data(ttl=300)
def get_weather_data(city="São Paulo"):
    try:
        response = requests.get(f"{API_BASE_URL}/weather/{city}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@st.cache_data(ttl=300)
def get_weather_forecast(city="São Paulo"):
    try:
        response = requests.get(f"{API_BASE_URL}/weather/forecast/{city}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_irrigation_status():
    try:
        response = requests.get(f"{API_BASE_URL}/irrigation/status")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_soil_health():
    try:
        response = requests.get(f"{API_BASE_URL}/analysis/soil-health")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_dashboard_summary():
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/summary")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Header principal
st.markdown('<h1 class="main-header">🌱 AgroSmart Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
selected_city = st.sidebar.selectbox("Localização", ["São Paulo", "Campinas", "Ribeirão Preto", "Piracicaba"])

if auto_refresh:
    time.sleep(30)
    st.rerun()

# Resumo geral
summary = get_dashboard_summary()
if summary:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sensores Ativos", f"{summary['active_sensors']}/{summary['total_sensors']}")
    with col2:
        st.metric("Zonas de Irrigação", summary['irrigation_zones'])
    with col3:
        st.metric("Irrigações Ativas", summary['active_irrigations'])
    with col4:
        st.metric("Status Geral", "✅ Online")

# Alertas
if summary and summary.get('alerts'):
    st.subheader("🚨 Alertas do Sistema")
    for alert in summary['alerts']:
        if alert['type'] == 'warning':
            st.markdown(f'<div class="alert-warning">⚠️ {alert["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-info">ℹ️ {alert["message"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# Layout em abas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Monitoramento", "🌤️ Clima", "💧 Irrigação", "🌱 Análise", "🔮 Predição"])

with tab1:
    st.subheader("📊 Monitoramento de Sensores em Tempo Real")
    
    sensors_data = get_sensors_data()
    
    if sensors_data:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        avg_temp = sum(s['temperature'] for s in sensors_data) / len(sensors_data)
        avg_humidity = sum(s['humidity'] for s in sensors_data) / len(sensors_data)
        avg_moisture = sum(s['soil_moisture'] for s in sensors_data) / len(sensors_data)
        avg_ph = sum(s['ph_level'] for s in sensors_data) / len(sensors_data)
        
        with col1:
            st.metric("Temperatura Média", f"{avg_temp:.1f}°C")
        with col2:
            st.metric("Umidade do Ar", f"{avg_humidity:.1f}%")
        with col3:
            st.metric("Umidade do Solo", f"{avg_moisture:.1f}%")
        with col4:
            st.metric("pH Médio", f"{avg_ph:.1f}")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de temperatura por sensor
            df_sensors = pd.DataFrame(sensors_data)
            fig_temp = px.bar(df_sensors, x='sensor_id', y='temperature', 
                             title='Temperatura por Sensor',
                             color='temperature',
                             color_continuous_scale='RdYlBu_r')
            fig_temp.update_layout(height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            # Gráfico de umidade do solo
            fig_moisture = px.bar(df_sensors, x='sensor_id', y='soil_moisture',
                                title='Umidade do Solo por Sensor',
                                color='soil_moisture',
                                color_continuous_scale='Blues')
            fig_moisture.update_layout(height=400)
            st.plotly_chart(fig_moisture, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("Dados Detalhados dos Sensores")
        df_display = df_sensors[['sensor_id', 'temperature', 'humidity', 'soil_moisture', 'ph_level']]
        st.dataframe(df_display, use_container_width=True)
        
    else:
        st.warning("Não foi possível carregar dados dos sensores. Verifique se a API está rodando.")

with tab2:
    st.subheader("🌤️ Condições Meteorológicas")
    
    weather_data = get_weather_data(selected_city)
    
    if weather_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Temperatura", f"{weather_data['temperature']:.1f}°C")
            st.metric("Umidade", f"{weather_data['humidity']:.1f}%")
        
        with col2:
            st.metric("Pressão", f"{weather_data['pressure']:.1f} hPa")
            st.metric("Vento", f"{weather_data['wind_speed']:.1f} km/h")
        
        with col3:
            st.metric("Condição", weather_data['description'])
            st.metric("Local", weather_data['location'])
        
        # Previsão do tempo
        forecast_data = get_weather_forecast(selected_city)
        
        if forecast_data:
            st.subheader("📅 Previsão para os Próximos 5 Dias")
            
            forecast_df = pd.DataFrame(forecast_data['forecast'])
            
            # Gráfico de previsão
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['date'], 
                y=forecast_df['temperature_max'],
                mode='lines+markers',
                name='Temp. Máxima',
                line=dict(color='red')
            ))
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['date'], 
                y=forecast_df['temperature_min'],
                mode='lines+markers',
                name='Temp. Mínima',
                line=dict(color='blue')
            ))
            fig_forecast.update_layout(title='Previsão de Temperatura', height=400)
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Tabela de previsão
            st.dataframe(forecast_df, use_container_width=True)
    
    else:
        st.warning("Não foi possível carregar dados meteorológicos.")

with tab3:
    st.subheader("💧 Sistema de Irrigação")
    
    irrigation_status = get_irrigation_status()
    
    if irrigation_status:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Zonas Ativas", irrigation_status['active_zones'])
        with col2:
            st.metric("Total de Zonas", irrigation_status['total_zones'])
        with col3:
            st.metric("Uso de Água Hoje", f"{irrigation_status['water_usage_today']:.1f}L")
        with col4:
            st.metric("Eficiência", f"{irrigation_status['efficiency_score']:.1f}%")
        
        # Controles de irrigação
        st.subheader("🎮 Controles de Irrigação")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            zone_id = st.selectbox("Zona", [f"Zona {i}" for i in range(1, 6)])
        with col2:
            duration = st.number_input("Duração (minutos)", min_value=5, max_value=120, value=30)
        with col3:
            auto_mode = st.checkbox("Modo Automático")
        
        if st.button("🚰 Ativar Irrigação"):
            try:
                response = requests.post(f"{API_BASE_URL}/irrigation/activate", 
                                       json={
                                           "zone_id": zone_id,
                                           "duration_minutes": duration,
                                           "auto_mode": auto_mode
                                       })
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                    st.info(f"Conclusão estimada: {result['estimated_completion']}")
                else:
                    st.error("Erro ao ativar irrigação")
            except:
                st.error("Erro de conexão com a API")
    
    else:
        st.warning("Não foi possível carregar status da irrigação.")

with tab4:
    st.subheader("🌱 Análise da Saúde do Solo")
    
    soil_health = get_soil_health()
    
    if soil_health:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score de Saúde", f"{soil_health['health_score']}/100")
        with col2:
            st.metric("Status", soil_health['status'])
        with col3:
            color = "green" if soil_health['health_score'] >= 80 else "orange" if soil_health['health_score'] >= 60 else "red"
            st.markdown(f"<h3 style='color: {color}'>{'🟢' if color=='green' else '🟠' if color=='orange' else '🔴'}</h3>", unsafe_allow_html=True)
        
        # Medições
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("pH Médio", soil_health['average_ph'])
        with col2:
            st.metric("Umidade Média", f"{soil_health['average_moisture']:.1f}%")
        
        # Recomendações
        st.subheader("📋 Recomendações")
        for i, rec in enumerate(soil_health['recommendations'], 1):
            st.write(f"{i}. {rec}")
        
        # Gráfico de saúde do solo
        categories = ['pH', 'Umidade', 'Nutrientes', 'Estrutura']
        values = [
            85 if 6.0 <= soil_health['average_ph'] <= 7.0 else 60,
            min(soil_health['average_moisture'] * 1.2, 100),
            75,  # Simulado
            80   # Simulado
        ]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Saúde do Solo'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Análise Multidimensional do Solo"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    else:
        st.warning("Não foi possível carregar análise do solo.")

with tab5:
    st.subheader("🔮 Predição de Safra")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_type = st.selectbox("Tipo de Cultura", 
                                ["milho", "soja", "trigo", "arroz", "feijao"])
        area = st.number_input("Área (hectares)", min_value=0.1, max_value=1000.0, value=10.0, step=0.1)
    
    with col2:
        st.info("💡 **Como funciona?**\n\nO modelo de predição considera:\n- Dados históricos de produtividade\n- Condições climáticas atuais\n- Saúde do solo\n- Padrões sazonais")
    
    if st.button("📊 Gerar Predição"):
        try:
            response = requests.post(f"{API_BASE_URL}/analysis/crop-prediction",
                                   params={"crop_type": crop_type, "area_hectares": area})
            
            if response.status_code == 200:
                prediction = response.json()
                
                st.success("✅ Predição gerada com sucesso!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Produtividade Estimada", f"{prediction['predicted_yield']:.1f} ton")
                with col2:
                    st.metric("Confiança do Modelo", f"{prediction['confidence']:.1f}%")
                with col3:
                    st.metric("Cultura", prediction['crop_type'].title())
                
                # Recomendações
                st.subheader("📋 Recomendações Técnicas")
                for i, rec in enumerate(prediction['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                
                # Gráfico de comparação
                benchmark_yield = {
                    "milho": 8.5, "soja": 3.2, "trigo": 4.8, 
                    "arroz": 6.1, "feijao": 2.8
                }.get(crop_type, 5.0) * area
                
                comparison_data = {
                    'Cenário': ['Média Regional', 'Predição AgroSmart'],
                    'Produtividade': [benchmark_yield, prediction['predicted_yield']]
                }
                
                df_comparison = pd.DataFrame(comparison_data)
                fig_comparison = px.bar(df_comparison, x='Cenário', y='Produtividade',
                                      title='Comparação de Produtividade (toneladas)',
                                      color='Cenário')
                st.plotly_chart(fig_comparison, use_container_width=True)
                
            else:
                st.error("Erro ao gerar predição")
        except:
            st.error("Erro de conexão com a API")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🌱 <strong>AgroSmart Dashboard</strong> - Sistema Inteligente de Automação Agrícola</p>
    <p>Desenvolvido com FastAPI + Streamlit | Última atualização: {}</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

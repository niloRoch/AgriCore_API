from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import random
from datetime import datetime, timedelta
import asyncio
import uvicorn

app = FastAPI(
    title="AgroSmart API",
    description="API de Automação Inteligente para Agricultura",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    soil_moisture: float
    ph_level: float
    timestamp: datetime

class WeatherData(BaseModel):
    location: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    description: str
    timestamp: datetime

class IrrigationCommand(BaseModel):
    zone_id: str
    duration_minutes: int
    auto_mode: bool = False

class CropPrediction(BaseModel):
    crop_type: str
    area_hectares: float
    predicted_yield: float
    confidence: float
    recommendations: List[str]

# Simulação de banco de dados em memória
sensors_data = []
irrigation_logs = []
weather_cache = {}

# Configurações de APIs externas
OPENWEATHER_API_KEY = "demo_key"  # Substitua pela sua chave real
NASA_API_KEY = "DEMO_KEY"  # Substitua pela sua chave real

@app.get("/")
async def root():
    return {"message": "AgroSmart API - Sistema de Automação Agrícola"}

# === ROTAS DE SENSORES ===
@app.get("/sensors/current", response_model=List[SensorData])
async def get_current_sensors():
    """Retorna dados atuais de todos os sensores"""
    # Simulação de 5 sensores diferentes
    current_sensors = []
    for i in range(1, 6):
        sensor = SensorData(
            sensor_id=f"AGRO_{i:03d}",
            temperature=round(random.uniform(18, 35), 1),
            humidity=round(random.uniform(45, 85), 1),
            soil_moisture=round(random.uniform(20, 80), 1),
            ph_level=round(random.uniform(5.5, 7.5), 1),
            timestamp=datetime.now()
        )
        current_sensors.append(sensor)
        
    sensors_data.extend(current_sensors)
    return current_sensors

@app.post("/sensors/data")
async def receive_sensor_data(sensor: SensorData):
    """Recebe dados de sensores IoT"""
    sensors_data.append(sensor)
    
    # Verificar alertas automáticos
    alerts = []
    if sensor.soil_moisture < 30:
        alerts.append("Baixa umidade do solo - Irrigação recomendada")
    if sensor.ph_level < 6.0 or sensor.ph_level > 7.0:
        alerts.append("pH do solo fora da faixa ideal")
    if sensor.temperature > 32:
        alerts.append("Temperatura alta - Monitorar stress térmico")
    
    return {"status": "success", "alerts": alerts}

# === ROTAS DE CLIMA ===
@app.get("/weather/{city}", response_model=WeatherData)
async def get_weather(city: str):
    """Obtém dados meteorológicos usando OpenWeather API"""
    try:
        # API real do OpenWeather (requer chave válida)
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        # Para demo, vamos simular a resposta
        weather_data = WeatherData(
            location=city,
            temperature=round(random.uniform(20, 30), 1),
            humidity=round(random.uniform(50, 80), 1),
            pressure=round(random.uniform(1010, 1025), 1),
            wind_speed=round(random.uniform(0, 15), 1),
            description=random.choice(["Clear sky", "Few clouds", "Scattered clouds", "Light rain"]),
            timestamp=datetime.now()
        )
        
        weather_cache[city] = weather_data
        return weather_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados meteorológicos: {str(e)}")

@app.get("/weather/forecast/{city}")
async def get_weather_forecast(city: str):
    """Previsão do tempo para 5 dias"""
    forecast = []
    for i in range(5):
        day_data = {
            "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            "temperature_max": round(random.uniform(25, 35), 1),
            "temperature_min": round(random.uniform(15, 25), 1),
            "humidity": round(random.uniform(50, 80), 1),
            "precipitation": round(random.uniform(0, 10), 1),
            "description": random.choice(["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Heavy rain"])
        }
        forecast.append(day_data)
    
    return {"city": city, "forecast": forecast}

# === ROTAS DE IRRIGAÇÃO ===
@app.post("/irrigation/activate")
async def activate_irrigation(command: IrrigationCommand):
    """Ativa sistema de irrigação"""
    irrigation_log = {
        "zone_id": command.zone_id,
        "start_time": datetime.now(),
        "duration_minutes": command.duration_minutes,
        "auto_mode": command.auto_mode,
        "status": "active"
    }
    
    irrigation_logs.append(irrigation_log)
    
    return {
        "message": f"Irrigação ativada na zona {command.zone_id}",
        "duration": command.duration_minutes,
        "estimated_completion": datetime.now() + timedelta(minutes=command.duration_minutes)
    }

@app.get("/irrigation/status")
async def get_irrigation_status():
    """Status atual dos sistemas de irrigação"""
    active_zones = [log for log in irrigation_logs if log["status"] == "active"]
    
    return {
        "active_zones": len(active_zones),
        "total_zones": 5,
        "water_usage_today": round(random.uniform(100, 500), 1),
        "efficiency_score": round(random.uniform(80, 95), 1),
        "active_systems": active_zones[-3:] if active_zones else []
    }

# === ROTAS DE ANÁLISE E PREDIÇÃO ===
@app.post("/analysis/crop-prediction", response_model=CropPrediction)
async def predict_crop_yield(crop_type: str, area_hectares: float):
    """Predição de rendimento da cultura usando ML simulado"""
    
    # Simulação de modelo de ML
    base_yield = {
        "milho": 8.5,
        "soja": 3.2,
        "trigo": 4.8,
        "arroz": 6.1,
        "feijao": 2.8
    }.get(crop_type.lower(), 5.0)
    
    # Fatores de ajuste baseados em condições simuladas
    weather_factor = random.uniform(0.85, 1.15)
    soil_factor = random.uniform(0.9, 1.1)
    
    predicted_yield = base_yield * weather_factor * soil_factor * area_hectares
    confidence = random.uniform(78, 92)
    
    # Recomendações baseadas nas condições
    recommendations = []
    if weather_factor < 0.95:
        recommendations.append("Considerar irrigação adicional devido ao clima seco")
    if soil_factor < 0.98:
        recommendations.append("Análise de solo recomendada para correção nutricional")
    recommendations.append("Monitorar pragas e doenças semanalmente")
    
    return CropPrediction(
        crop_type=crop_type,
        area_hectares=area_hectares,
        predicted_yield=round(predicted_yield, 2),
        confidence=round(confidence, 1),
        recommendations=recommendations
    )

@app.get("/analysis/soil-health")
async def get_soil_health_analysis():
    """Análise da saúde do solo baseada nos sensores"""
    if not sensors_data:
        raise HTTPException(status_code=404, detail="Nenhum dado de sensor disponível")
    
    recent_data = sensors_data[-5:]  # Últimos 5 registros
    
    avg_ph = sum(s.ph_level for s in recent_data) / len(recent_data)
    avg_moisture = sum(s.soil_moisture for s in recent_data) / len(recent_data)
    
    # Classificação da saúde do solo
    health_score = 0
    if 6.0 <= avg_ph <= 7.0:
        health_score += 30
    if avg_moisture >= 40:
        health_score += 40
    health_score += random.randint(20, 30)  # Outros fatores
    
    status = "Excelente" if health_score >= 85 else "Bom" if health_score >= 70 else "Regular"
    
    return {
        "health_score": health_score,
        "status": status,
        "average_ph": round(avg_ph, 2),
        "average_moisture": round(avg_moisture, 1),
        "recommendations": [
            "Manter programa regular de análise de solo",
            "Considerar rotação de culturas",
            "Monitorar níveis de matéria orgânica"
        ]
    }

@app.get("/dashboard/summary")
async def get_dashboard_summary():
    """Resumo geral para o dashboard"""
    return {
        "total_sensors": 5,
        "active_sensors": 5,
        "irrigation_zones": 5,
        "active_irrigations": len([log for log in irrigation_logs if log["status"] == "active"]),
        "last_update": datetime.now(),
        "alerts": [
            {"type": "info", "message": "Sistema funcionando normalmente"},
            {"type": "warning", "message": "Zona 3 com baixa umidade do solo"}
        ],
        "weather_status": "Parcialmente nublado, 25°C"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

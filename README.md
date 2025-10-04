# 🌱 AgroSmart - Sistema de Automação Agrícola

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-00a393.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-ff6b6b.svg)
![Docker](https://img.shields.io/badge/Docker-ready-0db7ed.svg)

API completa para automação agrícola com dashboard interativo, desenvolvida com FastAPI e Streamlit.

## 🚀 Características

### 🔧 Backend (FastAPI)
- **Monitoramento de Sensores**: Temperature, umidade, pH do solo
- **Integração Climática**: Dados meteorológicos em tempo real
- **Sistema de Irrigação**: Controle automatizado de irrigação
- **Análise de Solo**: Avaliação da saúde do solo
- **Predição de Safras**: Modelos de ML para previsão de produtividade
- **Documentação Automática**: Swagger UI integrado

### 🎨 Frontend (Streamlit)
- **Dashboard Interativo**: Visualizações em tempo real
- **Gráficos Avançados**: Plotly para visualizações dinâmicas
- **Controles de Irrigação**: Interface para ativação manual/automática
- **Análises Preditivas**: Predições de safra com recomendações
- **Monitoramento Climático**: Previsões e alertas meteorológicos

## 🛠️ Instalação Rápida

### 📋 Pré-requisitos
- Python 3.11+
- Docker & Docker Compose (opcional)
- Git

### 🐳 Opção 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agrosmart-api.git
cd agrosmart-api

# Execute com Docker Compose
docker-compose up --build
```

### 💻 Opção 2: Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agrosmart-api.git
cd agrosmart-api

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (novo terminal)
cd ../frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🌐 URLs de Acesso

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Dashboard** | http://localhost:8501 | Interface principal |
| **API** | http://localhost:8000 | Endpoints da API |
| **Documentação** | http://localhost:8000/docs | Swagger UI |
| **Redoc** | http://localhost:8000/redoc | Documentação alternativa |

## 🔗 Endpoints da API

### 📊 Sensores
```http
GET    /sensors/current           # Dados atuais dos sensores
POST   /sensors/data             # Enviar dados de sensores
```

### 🌤️ Clima
```http
GET    /weather/{city}           # Dados meteorológicos atuais
GET    /weather/forecast/{city}  # Previsão de 5 dias
```

### 💧 Irrigação
```http
POST   /irrigation/activate      # Ativar irrigação
GET    /irrigation/status        # Status do sistema de irrigação
```

### 🔬 Análise
```http
POST   /analysis/crop-prediction # Predição de safra
GET    /analysis/soil-health     # Análise da saúde do solo
```

### 📈 Dashboard
```http
GET    /dashboard/summary        # Resumo geral do sistema
```

## 📊 Funcionalidades do Dashboard

### 1. 📊 Monitoramento
- ✅ Visualização em tempo real de sensores
- ✅ Gráficos de temperatura, umidade e pH
- ✅ Alertas automáticos
- ✅ Tabela detalhada dos dados

### 2. 🌤️ Clima
- ✅ Condições meteorológicas atuais
- ✅ Previsão para 5 dias
- ✅ Gráficos de tendência de temperatura
- ✅ Seleção de diferentes cidades

### 3. 💧 Irrigação
- ✅ Status de todas as zonas
- ✅ Controles manuais de ativação
- ✅ Monitoramento de consumo de água
- ✅ Scores de eficiência

### 4. 🌱 Análise
- ✅ Score de saúde do solo
- ✅ Análise multidimensional (radar chart)
- ✅ Recomendações técnicas personalizadas
- ✅ Métricas de pH e umidade

### 5. 🔮 Predição
- ✅ Modelos de ML para 5 tipos de safras
- ✅ Comparações com médias regionais
- ✅ Nivel de confiança do modelo
- ✅ Recomendações baseadas em dados

## 🔧 Configuração Avançada

### 🌍 APIs Externas (Opcional)

Para usar dados reais, configure suas chaves de API:

1. **OpenWeather API**
   - Registre-se em: https://openweathermap.org/api
   - Obtenha sua chave gratuita
   - Configure no `.env`:
   ```bash
   OPENWEATHER_API_KEY=sua_chave_aqui
   ```

2. **NASA API**
   - Registre-se em: https://api.nasa.gov/
   - Configure no `.env`:
   ```bash
   NASA_API_KEY=sua_chave_aqui
   ```

### 🎯 Variáveis de Ambiente

```bash
# Copie o arquivo exemplo
cp .env.example .env

# Edite com suas configurações
nano .env
```

## 🏗️ Estrutura do Projeto

```
agrosmart-api/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Aplicação principal
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile         # Container backend
├── frontend/               # Streamlit Frontend  
│   ├── streamlit_app.py   # Dashboard principal
│   ├── requirements.txt   # Dependências frontend
│   └── Dockerfile        # Container frontend
├── docs/                  # Documentação
├── tests/                # Testes automatizados
├── data/                 # Dados de exemplo
├── docker-compose.yml    # Orquestração Docker
├── .env.example         # Configurações exemplo
└── README.md           # Este arquivo
```

## 🎯 Casos de Uso

| Setor | Aplicação |
|-------|-----------|
| **🌾 Agricultura de Precisão** | Monitoramento detalhado de cultivos |
| **💧 Gestão Hídrica** | Otimização do uso de água na irrigação |
| **📊 Analytics Agrícola** | Análise preditiva de safras |
| **🏭 Fazendas Verticais** | Controle de ambiente controlado |
| **🔬 Pesquisa** | Coleta e análise de dados experimentais |
| **📱 AgTech** | Base para aplicativos móveis |

## 🚀 Deploy em Produção

### 🌩️ Heroku
```bash
# Instalar Heroku CLI
heroku create agrosmart-api
git push heroku main
```

### ☁️ AWS/GCP
```bash
# Use os Dockerfiles inclusos
docker build -t agrosmart-api-backend ./backend
docker build -t agrosmart-api-frontend ./frontend
```

### 🔄 CI/CD
GitHub Actions configurado em `.github/workflows/`

## 📈 Roadmap

### Versão 2.0 🎯
- [ ] 🔐 Sistema de autenticação JWT
- [ ] 📱 API mobile (React Native)
- [ ] 🛰️ Integração com imagens de satélite
- [ ] 📊 Dashboard administrativo
- [ ] 💾 Banco de dados PostgreSQL

### Versão 3.0 🚀
- [ ] 🤖 IA avançada com TensorFlow
- [ ] 📡 Integração IoT real (LoRaWAN)
- [ ] 📧 Sistema de notificações
- [ ] 🏪 Marketplace de dados
- [ ] 🌍 Multi-idiomas

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -am 'Add: nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Abra** um Pull Request

### 📝 Padrões de Commit
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: manutenção
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend  
cd frontend
streamlit run streamlit_app.py --headless
```

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

--

<div align="center">

![AgroSmart](https://img.shields.io/badge/AgroSmart-2024-green?style=for-the-badge&logo=agriculture)

</div>

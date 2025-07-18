# 🌤️ MCP Weather Forecasting Agent

A sophisticated **Model Context Protocol (MCP)** agent that provides advanced weather forecasting capabilities using machine learning models, real-time weather data, and multiple AI tools integrated through the MCP framework.

## 🚀 Overview

This project implements a powerful weather forecasting system that combines:
- **Real-time weather data** from WeatherAPI
- **Machine learning models** for advanced predictions
- **Multiple AI tools** (crypto, web search, Wikipedia, etc.)
- **MCP (Model Context Protocol)** for seamless tool integration
- **Groq AI** for natural language processing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Side   │◄──►│   MCP Server    │◄──►│   AI Services   │
│  (Groq + MCP)   │    │   (FastMCP)     │    │ (APIs & Models) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ User Interface  │    │   Tool Manager  │    │  External APIs  │
│    & Queries    │    │   & Registry    │    │ & ML Models     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
MCPAgent/
├── 📄 ClientSide-SSE-MCP.py      # Main client application
├── 📄 ServerSideMCP.py           # MCP server entry point
├── 📁 MCPTools/                  # Core tools and services
│   ├── 📄 server.py              # FastMCP server configuration
│   ├── 📁 get_weather/           # Weather data processing
│   │   └── 📄 getweather.py      # Weather API integration
│   ├── 📁 loader/                # ML models and API clients
│   │   ├── 📄 loader.py          # Resource loader
│   │   └── 📁 ML-models/         # Pre-trained ML models
│   │       ├── 🤖 voting_regressor.joblib
│   │       ├── 🔧 feature_scaler.joblib
│   │       └── 🔧 target_scaler.joblib
│   └── 📁 tools/                 # Available MCP tools
│       ├── 🌤️ weather.py         # Weather forecasting
│       ├── 💰 trade.py           # Cryptocurrency data
│       ├── 🔍 web_search.py      # Web search capabilities
│       ├── 📚 wiki.py            # Wikipedia integration
│       ├── 📖 manga.py           # Manga information
│       ├── 🏓 ping.py            # System utilities
│       └── 🛠️ utils.py           # Helper functions
├── 📄 .gitignore                 # Git ignore rules
└── 📄 .env.example              # Environment variables template
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- API keys for various services

### 1. Clone & Install Dependencies
```bash
git clone <repository-url>
cd MCPAgent
pip install -r requirements.txt  # You may need to create this
```

### 2. Required Dependencies
```bash
pip install mcp
pip install groq
pip install pandas
pip install requests
pip install joblib
pip install python-dotenv
pip install tavily-python
pip install firecrawl-py
pip install openai
```

### 3. Environment Configuration
Create a `.env` file with the following API keys:

```env
# AI Services
GROQ_API_KEY_2=your_groq_api_key_here
OPENROUTER=your_openrouter_api_key

# Weather Service
WEATHER_API_KEY=your_weatherapi_key

# Search Services
TAVILY_API_KEY=your_tavily_key
GOOGLE_SEARCH_API_KEY=your_google_search_key
PROGRAMMABLE_SEARCH_ENGINE_ID=your_search_engine_id
FIRECRAWL_SANE_API=your_firecrawl_key

# Financial Data
ALPHAVANTAGE_API=your_alphavantage_key
```

### 4. API Key Setup Guide

| Service | Description | How to Get |
|---------|-------------|------------|
| **Groq** | Fast AI inference | [groq.com](https://groq.com) → Console → API Keys |
| **WeatherAPI** | Weather data | [weatherapi.com](https://weatherapi.com) → Free tier available |
| **Tavily** | AI search | [tavily.com](https://tavily.com) → Sign up for API |
| **Firecrawl** | Web scraping | [firecrawl.dev](https://firecrawl.dev) → Get API key |
| **Google Search** | Custom search | [Google Cloud Console](https://console.cloud.google.com) → Custom Search API |
| **AlphaVantage** | Financial data | [alphavantage.co](https://alphavantage.co) → Free API key |

## 🚀 Usage

### Quick Start
```bash
# Run the MCP weather agent
python ClientSide-SSE-MCP.py
```

### Example Queries

#### 🌤️ Weather Forecasting
```
"What's the weather like in London?"
"Give me a 5-day forecast for New York"
"Show me hourly weather for tomorrow in Paris"
"What's the air quality in Tokyo right now?"
```

#### 💰 Cryptocurrency Data
```
"What's the current Bitcoin price?"
"Show me Ethereum trading data"
```

#### 🔍 Research & Information
```
"Search for recent climate change news"
"Find information about machine learning in weather prediction"
"What's happening with renewable energy stocks?"
```

#### 📚 Knowledge Queries
```
"Tell me about meteorology from Wikipedia"
"Search for the latest manga releases"
```

## 🛠️ Available Tools

### Core Weather Tools
- **`get_weather()`** - Current weather and forecasts
  - Supports current conditions, daily/hourly forecasts
  - Air quality monitoring
  - Severe weather alerts
  - Multiple forecast types (daily/hourly)

### Financial Tools
- **`get_bitcoin_price()`** - Real-time Bitcoin pricing
- **`get_crypto_data()`** - Comprehensive cryptocurrency data

### Search & Research Tools
- **`deep_research()`** - AI-powered research assistant
- **`internet_search()`** - Google search integration
- **`search_firecrawl()`** - Advanced web scraping
- **`wikipedia_search()`** - Wikipedia knowledge base

### Utility Tools
- **`get_datetime()`** - Date and time utilities
- **`get_project_structure()`** - Project analysis
- **`get_credits()`** - System information
- **`get_summarized_manga_info()`** - Manga database queries

## 🔧 Advanced Configuration

### Custom Model Usage
```python
# Initialize with different AI models
client = MCPGroqClient(model="deepseek-ai/DeepSeek-V3")
# or
client = MCPGroqClient(model="llama3-8b-8192")
```

### Weather Forecast Types
```python
# Daily forecast
get_weather("London", forecast=True, days=5, forecast_type="daily")

# Hourly forecast
get_weather("Paris", forecast=True, days=3, forecast_type="hourly", day_for_hourly=1)

# Current weather with air quality
get_weather("Tokyo", current=True)
```

## 🧠 Machine Learning Models

The project includes pre-trained ML models for enhanced weather prediction:

- **`voting_regressor.joblib`** - Ensemble model for weather prediction
- **`feature_scaler.joblib`** - Input feature normalization
- **`target_scaler.joblib`** - Output scaling for predictions

These models work in conjunction with real-time API data to provide more accurate forecasts.

## 🔌 MCP (Model Context Protocol) Integration

This project leverages MCP for:
- **Tool Registration** - Automatic discovery of available functions
- **Type Safety** - Structured parameter validation
- **Scalable Architecture** - Easy addition of new tools
- **Client-Server Communication** - Robust messaging protocol

## 🌐 API Integrations

| Service | Purpose | Documentation |
|---------|---------|--------------|
| WeatherAPI | Weather data & forecasts | [docs.weatherapi.com](https://docs.weatherapi.com) |
| Groq | Fast AI inference | [docs.groq.com](https://docs.groq.com) |
| Tavily | AI-powered search | [docs.tavily.com](https://docs.tavily.com) |
| Firecrawl | Web scraping | [docs.firecrawl.dev](https://docs.firecrawl.dev) |
| AlphaVantage | Financial data | [alphavantage.co/documentation](https://alphavantage.co/documentation) |

## 🎯 Key Features

- ✅ **Real-time Weather Data** - Current conditions and forecasts
- ✅ **ML-Enhanced Predictions** - Machine learning model integration
- ✅ **Multi-tool Integration** - Crypto, search, research capabilities
- ✅ **Natural Language Interface** - Conversational AI interactions
- ✅ **Air Quality Monitoring** - Environmental health data
- ✅ **Severe Weather Alerts** - Safety notifications
- ✅ **Flexible Forecast Types** - Daily, hourly, and custom ranges
- ✅ **Multiple AI Models** - Support for various LLMs
- ✅ **Extensible Architecture** - Easy to add new tools

## 🚨 Error Handling

The system includes robust error handling for:
- Invalid API keys
- Network connectivity issues
- Malformed queries
- API rate limiting
- Missing environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol) for the protocol framework
- [Groq](https://groq.com) for lightning-fast AI inference
- [WeatherAPI](https://weatherapi.com) for comprehensive weather data
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server implementation

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Failed to get weather data
   Solution: Check your .env file and ensure all API keys are valid
   ```

2. **Module Import Errors**
   ```
   Error: ModuleNotFoundError
   Solution: Install missing dependencies with pip install -r requirements.txt
   ```

3. **MCP Connection Issues**
   ```
   Error: Failed to connect to MCP server
   Solution: Ensure ServerSideMCP.py is accessible and Python path is correct
   ```

### Getting Help

- 📧 Create an issue in the repository
- 📖 Check the API documentation for individual services
- 🔍 Review error logs for specific error messages

---

**Made with ❤️ for better weather forecasting and AI tool integration** 
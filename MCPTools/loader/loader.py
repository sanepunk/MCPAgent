from tavily import TavilyClient
from dotenv import load_dotenv
import os
from firecrawl import FirecrawlApp
import joblib
import requests
from openai import OpenAI

abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
parent_dir = os.path.dirname(dir_path)
system_dir = os.path.dirname(parent_dir)
load_dotenv(os.path.join(system_dir, ".env"))
model = joblib.load(os.path.join(dir_path, "ML-models/voting_regressor.joblib"))
feature_scaler = joblib.load(os.path.join(dir_path, "ML-models/feature_scaler.joblib"))
target_scaler = joblib.load(os.path.join(dir_path, "ML-models/target_scaler.joblib"))

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
alphavantage_api_key = os.getenv("ALPHAVANTAGE_API")
weather_api_key = os.getenv("WEATHER_API_KEY")
search_api = os.getenv("GOOGLE_SEARCH_API_KEY")
programmable_search_engine_id = os.getenv("PROGRAMMABLE_SEARCH_ENGINE_ID")
firecrawl_api_key = os.getenv("FIRECRAWL_SANE_API")
firecrawl_web_search_app = FirecrawlApp(api_key=firecrawl_api_key)
open_router_open_api_client = OpenAI(api_key=os.getenv("OPENROUTER"), base_url="https://openrouter.ai/api/v1")
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader import *

from typing import Dict, Any
import requests
import pandas as pd

@mcp.tool()
def get_bitcoin_price(request: dict[str, Any]) -> dict[str, Any]:
    """
    Predicts Bitcoin closing price using ML model.

    Args:
        request (dict): Must include "Open", "High", and "Low" (float).
    Example:
        request = {"Open": 120334, "High": 13600, "Low": 10089}
    Returns:
        dict: Predicted closing price or error message.
    """
    try:
        # model = joblib.load("voting_regressor.joblib")
        # feature_scaler = joblib.load("feature_scaler.joblib")
        # target_scaler = joblib.load("target_scaler.joblib")
        features = pd.DataFrame({
			'Open': [float(request['Open'])],
			'High': [float(request['High'])],
			'Low': [float(request['Low'])],
		})
        features = feature_scaler.transform(features)
        target = model.predict(features).reshape(-1, 1)
        target = target_scaler.inverse_transform(target).item()
        return {"Closing Price given from the Machine Learning Model is": target}
    except Exception as e:
        return {"Unable to predict the closing price": str(e)}
    
@mcp.tool()
def get_crypto_data(symbol: str, date: str, market: str = "US"):
    """
    This function takes a crypto symbol, date, and market and returns the crypto data.
    It uses the Alpha Vantage API to get the crypto data.
    Args:
        symbol (str): The crypto symbol to be used.
        date (str): The date to be used.
        market (str): The market to be used.
        example: "BTC", "2025-01-01", "EUR"
    Returns:
        dict: A dictionary of the crypto data.
        {"open": str, "high": str, "low": str}
    """
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={alphavantage_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['Time Series (Digital Currency Daily)'][date]
        result = {
            "open": result['1. open'],
            "high": result['2. high'],
            "low": result['3. low']
            # "close": result['4. close'],
            # "volume": result['5. volume']
        }
        return result
    else:
        return {
            "error": response.json()['Error Message']
        }
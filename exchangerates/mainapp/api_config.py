"""
Configuration module.
This module contains environment variable loading and API URL definitions.
"""

from datetime import datetime
import os


api_key = os.getenv("API_KEY")

api_url = "http://api.exchangeratesapi.io/v1/"

params = {
    "access_key": api_key,
    "base": "EUR",
    "symbols": "USD,GBP,RON"
    }

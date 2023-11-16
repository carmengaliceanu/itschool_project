"""
Fetching data module.
This module contains functions for hisorical data and daily data.
"""

import requests
from datetime import timedelta


def fetch_historical_data(api_url, params, start_date, end_date):
    """
    Fetch historical exchange rate data from the API.
    Returns data.
    """
    historical_data = []

    current_date = start_date

    while current_date < end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        response = requests.get(f"{api_url}{date_str}", params=params)

        if response.status_code == 200:
            data = response.json()
            historical_data.append(data)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None

        current_date += timedelta(days=1)

    return historical_data


def fetch_daily_data(api_url, params, last_date):
    """
    Update the database with the latest exchange rate data for the following day.
    Returns data.
    """
    next_date = last_date + timedelta(days=1)
    date_str = next_date.strftime("%Y-%m-%d")

    response = requests.get(f"{api_url}{date_str}", params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
    

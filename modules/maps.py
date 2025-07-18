# modules/maps.py

import requests

def geocode_location(location: str, api_key: str) -> tuple:
    """
    Geocode a free-text location to (latitude, longitude) using OpenCage.

    Args:
        location (str): The city or address
        api_key (str): OpenCage API key

    Returns:
        tuple: (lat, lng) if found, else (None, None)
    """
    if not location:
        return None, None

    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        results = data.get("results")
        if results:
            coords = results[0]["geometry"]
            return coords["lat"], coords["lng"]
    except Exception as e:
        print(f"Geocode error: {e}")

    return None, None
# Map visualizations using pydeck or folium

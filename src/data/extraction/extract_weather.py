import os
import json
import csv
from datetime import datetime
import sys
from pathlib import Path

# Add the project root to PYTHONPATH
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.utils.api_client import OpenWeatherMapClient
except ImportError as e:
    print(f"Error importing utils: {e}")
    print(f"sys.path: {sys.path}")
    raise

from loguru import logger

def extract_and_save_weather():
    """
    Extract weather data using the OpenWeatherMap API and save it to the raw data folder as CSV
    """
    # Initialize API client
    client = OpenWeatherMapClient()
    
    # Create data directory if it doesn't exist
    raw_data_dir = project_root / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Define output file path
    output_file = raw_data_dir / "weather_data.csv"
    
    try:
        # Get locations from config and find Casablanca
        locations = client.get_locations()
        casablanca = next(loc for loc in locations if loc["name"] == "Casablanca")
        
        # Get weather for Casablanca
        response = client.get_latest_weather(casablanca["lat"], casablanca["lon"])
        logger.debug(f"Raw weather data: {response}")
        
        if response.get('message') != 'success' or 'data' not in response:
            raise ValueError("Invalid API response format")
            
        weather_data = response['data']
        
        # Flatten the nested JSON data for CSV format
        flattened_data = {
            'timestamp': datetime.fromtimestamp(weather_data['dt']).isoformat(),
            'location_name': weather_data['name'],
            'latitude': weather_data['coord']['lat'],
            'longitude': weather_data['coord']['lon'],
            # Main weather data
            'weather_main': weather_data['weather'][0]['main'],
            'weather_description': weather_data['weather'][0]['description'],
            'weather_icon': weather_data['weather'][0]['icon'],
            # Temperature data
            'temp': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'temp_min': weather_data['main']['temp_min'],
            'temp_max': weather_data['main']['temp_max'],
            # Pressure and humidity
            'pressure': weather_data['main']['pressure'],
            'humidity': weather_data['main']['humidity'],
            'sea_level': weather_data['main'].get('sea_level'),
            'ground_level': weather_data['main'].get('grnd_level'),
            # Wind data
            'wind_speed': weather_data['wind']['speed'],
            'wind_direction': weather_data['wind'].get('deg'),
            # Clouds and visibility
            'cloud_cover': weather_data['clouds']['all'],
            'visibility': weather_data.get('visibility'),
            # System data
            'country': weather_data['sys']['country'],
            'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).isoformat(),
            'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).isoformat(),
            'timezone': weather_data['timezone']
        }
        
        # Check if file exists to write headers
        file_exists = output_file.exists()
        
        # Write to CSV file
        mode = 'a' if file_exists else 'w'
        with open(output_file, mode, newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=flattened_data.keys())
            
            # Write headers if file is new or empty
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(flattened_data)
            
        logger.info(f"Successfully saved weather data to {output_file}")
        
    except Exception as e:
        logger.error(f"Error extracting weather data: {str(e)}")
        raise

if __name__ == "__main__":
    extract_and_save_weather()

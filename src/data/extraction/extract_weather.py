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
    from src.utils.api_client import AmbeeAPIClient
except ImportError as e:
    print(f"Error importing utils: {e}")
    print(f"sys.path: {sys.path}")
    raise

from loguru import logger

def extract_and_save_weather():
    """
    Extract weather data using the Ambee API and save it to the raw data folder as CSV
    """
    # Initialize API client
    client = AmbeeAPIClient()
    
    # Create data directory if it doesn't exist
    raw_data_dir = project_root / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Define output file path with timestamp
    #timestamp = datetime.now().strftime("%Y%m%d")
    output_file = raw_data_dir / f"weather_data.csv"
    
    try:
        # Get weather for Casablanca
        response = client.get_latest_weather(33.5731, -7.5898)
        logger.debug(f"Raw weather data: {response}")
        
        if response.get('message') != 'success' or 'data' not in response:
            raise ValueError("Invalid API response format")
            
        weather_data = response['data']
        current_time = datetime.now().isoformat()
        
        # Flatten the nested JSON data for CSV format
        flattened_data = {
            'timestamp': current_time,
            'temperature': weather_data.get('temperature', None),
            'humidity': weather_data.get('humidity', None),
            'wind_speed': weather_data.get('windSpeed', None),
            'wind_direction': weather_data.get('windBearing', None),
            'pressure': weather_data.get('pressure', None),
            'precipitation': weather_data.get('precipIntensity', None),
            'cloud_cover': weather_data.get('cloudCover', None),
            'dew_point': weather_data.get('dewPoint', None),
            'uv_index': weather_data.get('uvIndex', None),
            'visibility': weather_data.get('visibility', None),
            'apparent_temperature': weather_data.get('apparentTemperature', None),
            'summary': weather_data.get('summary', None),
            'lat': weather_data.get('lat', 33.5731),
            'lng': weather_data.get('lng', -7.5898)
        }
        
        # Check if file exists to write headers
        file_exists = output_file.exists()
        
        # Write to CSV file in append mode
        with open(output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=flattened_data.keys())
            
            # Write headers only if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(flattened_data)
            
        logger.info(f"Successfully saved weather data to {output_file}")
        
    except Exception as e:
        logger.error(f"Error extracting weather data: {str(e)}")
        raise

if __name__ == "__main__":
    extract_and_save_weather()

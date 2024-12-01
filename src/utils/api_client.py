import os
import yaml
import requests
from typing import Dict, Any
from retry import retry
from loguru import logger
from dotenv import load_dotenv

class AmbeeAPIClient:
    def __init__(self, config_path: str = "config/api_config.yaml"):
        """Initialize the Ambee API client with configuration."""
        # Load environment variables
        load_dotenv()
        
        self.config = self._load_config(config_path)
        self.base_url = self.config["ambee"]["base_url"]
        
        # Get headers with API key from environment
        self.headers = {
            "x-api-key": os.getenv("AMBEE_API_KEY"),
            "Content-type": "application/json"
        }
        
        if not self.headers["x-api-key"]:
            raise ValueError("AMBEE_API_KEY environment variable is not set")
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    @retry(tries=3, delay=5, backoff=2)
    def get_latest_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get latest weather data for a specific latitude and longitude.
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            Dict[str, Any]: Weather data response
        """
        endpoint = self.config["ambee"]["endpoints"]["latest_weather"]
        url = f"{self.base_url}{endpoint}"
        
        params = {
            "lat": lat,
            "lng": lng
        }
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.config["request"]["timeout"]
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    client = AmbeeAPIClient()
    try:
        # Get weather for Casablanca
        weather_data = client.get_latest_weather(33.5731, -7.5898)
        print("Weather data:", weather_data)
    except Exception as e:
        print(f"Error: {str(e)}")

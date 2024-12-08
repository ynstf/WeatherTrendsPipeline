import os
import yaml
import requests
import time
from typing import Dict, Any, Optional, List
from retry import retry
from loguru import logger
from dotenv import load_dotenv
from requests.exceptions import RequestException, Timeout, TooManyRedirects, HTTPError

class WeatherAPIError(Exception):
    """Base exception for weather API errors."""
    pass

class APIRateLimitError(WeatherAPIError):
    """Raised when API rate limit is exceeded."""
    pass

class APIConnectionError(WeatherAPIError):
    """Raised when connection to API fails."""
    pass

class APIResponseError(WeatherAPIError):
    """Raised when API returns an error response."""
    pass

class DataValidationError(WeatherAPIError):
    """Raised when received data fails validation."""
    pass

class OpenWeatherMapClient:
    def __init__(self, config_path: str = "config/api_config.yaml"):
        """Initialize the OpenWeatherMap API client with configuration."""
        # Load environment variables
        load_dotenv()
        
        self.config = self._load_config(config_path)
        self.base_url = self.config["openweathermap"]["base_url"]
        
        # Get API key from environment
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY environment variable is not set")
        
        # Load locations from config
        self.locations = self.config["locations"]
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, FileNotFoundError) as e:
            logger.error(f"Error loading config file: {str(e)}")
            raise WeatherAPIError(f"Configuration error: {str(e)}")

    def _validate_coordinates(self, lat: float, lng: float) -> None:
        """Validate latitude and longitude values."""
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            raise DataValidationError("Latitude and longitude must be numeric values")
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            raise DataValidationError("Invalid coordinates: latitude must be between -90 and 90, longitude between -180 and 180")

    def _validate_response_data(self, data: Dict[str, Any]) -> None:
        """Validate response data structure."""
        required_fields = ["coord", "weather", "main", "wind", "clouds", "sys"]
        if not all(field in data for field in required_fields):
            raise DataValidationError("Response data missing required fields")

    def get_locations(self) -> List[Dict[str, Any]]:
        """Get list of configured locations."""
        return self.locations

    @retry(exceptions=(APIConnectionError, Timeout), tries=3, delay=5, backoff=2, logger=logger)
    def get_latest_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get latest weather data for a specific latitude and longitude.
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            Dict[str, Any]: Complete weather data response
            
        Raises:
            APIConnectionError: When connection to API fails
            APIResponseError: When API returns an error response
            DataValidationError: When data validation fails
        """
        self._validate_coordinates(lat, lng)
        
        endpoint = self.config["openweathermap"]["endpoints"]["current_weather"]
        url = f"{self.base_url}{endpoint}"
        
        params = {
            "lat": lat,
            "lon": lng,
            "appid": self.api_key
        }
        
        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.config["request"]["timeout"]
            )
            
            # Handle different HTTP status codes
            if response.status_code == 401:
                raise APIResponseError("Invalid API key")
            elif response.status_code == 404:
                raise APIResponseError("Resource not found")
            elif response.status_code == 429:
                raise APIRateLimitError("API rate limit exceeded")
            
            response.raise_for_status()
            
            data = response.json()
            self._validate_response_data(data)
            
            # Add timestamp and success message
            result = {
                "message": "success",
                "timestamp": time.time(),
                "data": data
            }
            
            return result
            
        except Timeout:
            logger.error("Request timed out")
            raise APIConnectionError("Request timed out")
        except ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise APIConnectionError(f"Failed to connect to API: {str(e)}")
        except HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            raise APIResponseError(f"API returned error: {str(e)}")
        except RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise APIConnectionError(f"Request failed: {str(e)}")
        except ValueError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise DataValidationError(f"Invalid JSON response: {str(e)}")

if __name__ == "__main__":
    # Example usage
    client = OpenWeatherMapClient()
    try:
        # Get all configured locations
        locations = client.get_locations()
        
        # Get weather for each location
        for location in locations:
            weather = client.get_latest_weather(location["lat"], location["lon"])
            print(f"\nWeather for {location['name']}:")
            print(weather)
            
    except WeatherAPIError as e:
        logger.error(f"Weather API error: {str(e)}")

import os
import yaml
import requests
import time
from typing import Dict, Any, Optional
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
        
        # Initialize rate limiting parameters
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        
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
        required_fields = ["message", "data"]
        if not all(field in data for field in required_fields):
            raise DataValidationError("Response data missing required fields")

    def _update_rate_limits(self, response: requests.Response) -> None:
        """Update rate limit information from response headers."""
        self.rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
        self.rate_limit_reset = response.headers.get('X-RateLimit-Reset')

    def _handle_rate_limit(self) -> None:
        """Handle rate limiting by waiting if necessary."""
        if self.rate_limit_remaining == "0" and self.rate_limit_reset:
            wait_time = int(self.rate_limit_reset) - int(time.time())
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time} seconds.")
                time.sleep(wait_time + 1)  # Add 1 second buffer

    @retry(exceptions=(APIConnectionError, Timeout), tries=3, delay=5, backoff=2, logger=logger)
    def get_latest_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get latest weather data for a specific latitude and longitude.
        
        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Returns:
            Dict[str, Any]: Weather data response
            
        Raises:
            APIRateLimitError: When API rate limit is exceeded
            APIConnectionError: When connection to API fails
            APIResponseError: When API returns an error response
            DataValidationError: When data validation fails
        """
        self._validate_coordinates(lat, lng)
        self._handle_rate_limit()
        
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
            
            # Update rate limit info
            self._update_rate_limits(response)
            
            # Handle different HTTP status codes
            if response.status_code == 429:
                raise APIRateLimitError("API rate limit exceeded")
            elif response.status_code == 401:
                raise APIResponseError("Invalid API key")
            elif response.status_code == 404:
                raise APIResponseError("Resource not found")
            
            response.raise_for_status()
            
            data = response.json()
            self._validate_response_data(data)
            return data
            
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
    client = AmbeeAPIClient()
    try:
        # Get weather for Casablanca
        weather_data = client.get_latest_weather(33.5731, -7.5898)
        logger.info("Successfully retrieved weather data")
        logger.debug(f"Weather data: {weather_data}")
    except WeatherAPIError as e:
        logger.error(f"Weather API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

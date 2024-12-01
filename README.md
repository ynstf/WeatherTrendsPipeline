# WeatherTrendsPipeline

A comprehensive data engineering pipeline for collecting, processing, and analyzing weather data using the Ambee Weather API.

## Project Structure

```
WeatherTrendsPipeline/
├── src/                      # Source code
│   ├── data/                 # Data handling modules
│   │   ├── extraction/       # Data extraction scripts (API calls)
│   │   ├── processing/       # Data transformation scripts
│   │   └── storage/         # Database interaction scripts
│   ├── visualization/        # Visualization scripts
│   └── utils/               # Utility functions
├── config/                   # Configuration files
│   ├── db_config.yaml       # Database configuration
│   └── api_config.yaml      # API configuration
├── airflow/                  # Airflow DAGs and operators
│   ├── dags/                # DAG definitions
│   └── operators/           # Custom operators
├── tests/                   # Test files
├── notebooks/               # Jupyter notebooks for analysis
├── docs/                    # Documentation
├── data/                    # Data files
│   ├── raw/                 # Raw data
│   ├── processed/           # Processed data
│   └── final/              # Final analysis results
└── requirements.txt         # Project dependencies
```

## Setup

1. Clone the repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.template` to `.env` and add your Ambee API key:
   ```
   AMBEE_API_KEY=your_api_key_here
   ```
5. Copy `config/api_config.template.yaml` to `config/api_config.yaml`

## Usage Examples

### Getting Current Weather Data

```python
from src.utils.api_client import AmbeeAPIClient

# Initialize the client
client = AmbeeAPIClient()

# Get weather for Casablanca
casablanca_weather = client.get_latest_weather(33.5731, -7.5898)

# Example response:
{
    "message": "success",
    "data": {
        "temperature": 77,        # Temperature in Fahrenheit
        "humidity": 31,           # Humidity percentage
        "pressure": 1020,         # Pressure in mb
        "windSpeed": 3.3,         # Wind speed in mph
        "windBearing": 356,       # Wind direction in degrees
        "cloudCover": 0.69,       # Cloud cover (0-1)
        "uvIndex": 1,            # UV index
        "summary": "Partly cloudy skies. Temperatures will feel warm..."
    }
}

# Get weather for other Moroccan cities
rabat_weather = client.get_latest_weather(34.0209, -6.8416)
marrakech_weather = client.get_latest_weather(31.6295, -7.9811)
fez_weather = client.get_latest_weather(34.0181, -5.0078)
```

### Common Locations

| City       | Latitude  | Longitude |
|------------|-----------|-----------|
| Casablanca | 33.5731   | -7.5898   |
| Rabat      | 34.0209   | -6.8416   |
| Marrakech  | 31.6295   | -7.9811   |
| Fez        | 34.0181   | -5.0078   |

## Features

- Real-time weather data retrieval
- Secure API key management using environment variables
- Error handling and automatic retries
- Support for multiple Moroccan cities
- Comprehensive weather information including:
  - Temperature
  - Humidity
  - Wind speed and direction
  - Cloud cover
  - UV index
  - Atmospheric pressure
  - Weather conditions summary

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
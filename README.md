# WeatherTrendsPipeline

A comprehensive data engineering pipeline for collecting, processing, and analyzing weather data using the OpenWeatherMap API.

## Project Structure

```
WeatherTrendsPipeline/
├── src/                      # Source code
│   ├── data/                 # Data handling modules
│   │   ├── extraction/       # Data extraction scripts
│   │   │   └── extract_weather.py    # Weather data extraction
│   │   ├── processing/       # Data transformation scripts
│   │   │   └── transform_weather.py  # Weather data transformation
│   │   └── storage/          # Data storage scripts
│   │       └── load_weather.py       # S3 upload functionality
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── api_client.py    # API interaction utilities
│   │   ├── def_transformations.py  # Data transformation functions
│   │   └── save_data.py    # Data saving and management utilities
│   └── visualization/       # Data visualization components
├── data/                    # Data storage
│   ├── raw/                # Raw weather data
│   ├── processed/          # Transformed data
│   └── final/             # Final analysis results
├── config/                 # Configuration files
│   ├── db_config.yaml     # Database settings
│   └── api_config.yaml    # API settings
├── dags/                  # Automation scripts
│   ├── extraction.sh      # Data extraction shell script
│   └── trans_Load.sh      # Transformation and S3 upload script
├── scheduler/             # Scheduling configuration
│   └── CRON              # Cron job definitions
├── docs/                 # Documentation
│   ├── api_documentation.md    # API endpoints and usage
│   ├── data_schema.md         # Data structure definitions
│   └── pipeline_documentation.md  # Pipeline processes and monitoring
├── logs/                 # Log files
│   └── extraction.log  # Log file for extractions and uploads
├── notebooks/           # Jupyter notebooks
├── tests/              # Test files
├── .env               # Environment variables (including AWS credentials)
├── .env.template      # Environment variables template
├── requirements.txt  # Python dependencies
└── setup_venv.bat   # Virtual environment setup
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
4. Copy `.env.template` to `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
5. Copy `config/api_config.template.yaml` to `config/api_config.yaml`

## Usage Examples

### Getting Current Weather Data

```python
from src.utils.api_client import OpenWeatherMapAPIClient

# Initialize the client
client = OpenWeatherMapAPIClient()

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

## Data Processing Features

### Transformation Pipeline
- Comprehensive data transformation capabilities:
  - Temperature unit conversions (°F to °C)
  - Wind speed conversions (mph to km/h and m/s)
  - Pressure conversions (mb to hPa and atm)
  - Visibility distance conversions (miles to km)

### Advanced Weather Metrics
- Heat Index calculation for temperatures ≥ 80°F
- Wind Chill calculation for temperatures ≤ 50°F and wind speeds > 3 mph
- Seasonal categorization based on month
- Time-based analytics (hour, day, month patterns)

### Automated Scheduling
- Cron job implementation for automated data collection
- Shell script automation:
  ```bash
  # Extraction shell script (dags/extraction.sh)
  #!/bin/bash
  cd /WeatherTrendsPipeline
  source venv/bin/activate
  python src/data/extraction/extract_weather.py >> logs/extraction.log 2>&1
  ```
- Cron scheduling example:
  ```bash
  # Run every 14 minutes (optimized for 100 API calls per day limit)
  */14 * * * * /WeatherTrendsPipeline/dags/extraction.sh
  ```
- Logging system:
  ```
  logs/
  └── extraction.log  # Log file for extractions and uploads
  ```
  Log entries include:
  ```
  [2024-12-06 14:00:01] INFO: Starting weather data extraction
  [2024-12-06 14:00:02] INFO: Successfully retrieved weather data for Casablanca
  [2024-12-06 14:00:03] INFO: Data saved to /WeatherTrendsPipeline/data/raw/weather_data.csv
  [2024-12-06 14:14:01] INFO: Starting weather data extraction
  [2024-12-06 14:14:02] INFO: Successfully retrieved weather data for Casablanca
  [2024-12-06 14:14:03] INFO: Data saved to /WeatherTrendsPipeline/data/raw/weather_data.csv
  ...
  ```

### Data Storage Structure
- Raw data storage:
  - CSV format with timestamp-based naming
  - Automatic daily file management
- Processed data:
  - Enriched datasets with calculated metrics
  - Transformed units for analysis
  - Temporal features extraction
- Cloud Storage:
  - Automated daily uploads to AWS S3 bucket at 12:01
  - Processed data backup and archival
  - Automatic cleanup of local files after successful upload

### Automated Scheduling
- Daily S3 Upload Schedule:
  ```bash
  # Upload processed data to S3 bucket daily at 12:01
  1 12 * * * /WeatherTrendsPipeline/dags/upload_to_s3.sh
  ```

### Remote Deployment
- AWS EC2 instance deployment
- SSH Configuration:
  ```
  Host WeatherTrendsPipeline
      Hostname X.X.X.X
      User ubuntu
      IdentityFile "path/to/WeatherPipeline.pem"
  ```

### Error Handling and Logging
- Comprehensive error handling for:
  - API connection issues
  - Data validation
  - File operations
- Detailed logging system
- Automatic retry mechanisms

## Technical Requirements

### Python Environment
- Python version: 3.9.7
- Key dependencies:
  ```
  numpy==1.24.3
  pandas==2.0.3
  requests
  python-dotenv
  loguru
  ```

### System Requirements
- Linux/Unix environment for cron jobs
- Write permissions for data directories
- Network access for API calls
- SSH access for remote deployment

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
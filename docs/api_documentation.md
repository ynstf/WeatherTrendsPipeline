# API Documentation

## Ambee Weather API

### Endpoints
- Base URL: `https://api.ambeedata.com/weather/latest/by-lat-lng`
- Authentication: API key required in headers

### Request Format
```http
GET /weather/latest/by-lat-lng?lat={latitude}&lng={longitude}
Headers:
  x-api-key: YOUR_API_KEY
```

### Response Format
```json
{
    "message": "success",
    "data": {
        "temperature": 77,        // Temperature in Fahrenheit
        "humidity": 31,           // Humidity percentage
        "pressure": 1020,         // Pressure in mb
        "windSpeed": 3.3,         // Wind speed in mph
        "windBearing": 356,       // Wind direction in degrees
        "cloudCover": 0.69,       // Cloud cover (0-1)
        "uvIndex": 1             // UV index
    }
}
```

## AWS S3 Integration

### Bucket Structure
- Raw data: `{bucket_name}/raw/`
- Processed data: `{bucket_name}/processed/`
- Archive: `{bucket_name}/archive/`

### Access Requirements
- AWS Access Key ID
- AWS Secret Access Key
- Bucket permissions: read/write access

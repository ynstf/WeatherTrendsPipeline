# Pipeline Documentation

## Data Pipeline Overview

### 1. Data Extraction
- **Script**: `src/data/extraction/extract_weather.py`
- **Schedule**: Every 14 minutes
- **Process**:
  1. Fetches weather data from Ambee API
  2. Validates response data
  3. Saves raw data to CSV in `data/raw/`

### 2. Data Transformation
- **Script**: `src/data/processing/transform_weather.py`
- **Schedule**: Daily at 12:01
- **Transformations**:
  - Temperature conversion (°F to °C)
  - Wind speed conversion (mph to m/s)
  - Pressure conversion (mb to hPa)
  - Heat index calculation
  - Wind chill calculation
  - Season determination
  - Time-based feature extraction

### 3. Data Loading
- **Script**: `src/data/storage/load_weather.py`
- **Schedule**: Daily at 12:01 (after transformation)
- **Process**:
  1. Uploads processed data to S3
  2. Archives previous day's data
  3. Cleans up local storage

## Automation Scripts

### extraction.sh
```bash
#!/bin/bash
# Executes data extraction process
# Runs every 14 minutes via cron
```

### trans_Load.sh
```bash
#!/bin/bash
# Executes data transformation and S3 upload
# Runs daily at 12:01 via cron
```

## Error Handling

### Extraction Errors
- API connection failures: Retry with exponential backoff
- Data validation failures: Log error and skip invalid records
- File system errors: Alert and retry

### Transformation Errors
- Data type conversion: Apply safe conversion with defaults
- Missing data: Implement appropriate imputation strategies
- Calculation errors: Log and skip affected records

### Loading Errors
- S3 upload failures: Retry with exponential backoff
- File deletion errors: Log and alert for manual intervention
- Archive errors: Maintain local backup until successful upload

## Monitoring

### Logs
- Location: `logs/extraction.log`
- Contents:
  - API call results
  - Transformation statistics
  - S3 upload status
  - Error messages and stack traces

### Metrics
- API call success rate
- Data completeness
- Transformation accuracy
- Upload success rate
- Storage usage

#!/bin/bash

# Run the weather data extraction script
/home/ubuntu/WeatherTrendsPipeline/venv/bin/python /home/ubuntu/WeatherTrendsPipeline/src/data/extraction/extract_weather.py
# Log the extraction
echo "$(date) Weather data extraction completed" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log
echo "=========" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log

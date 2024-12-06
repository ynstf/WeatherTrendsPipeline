#!/bin/bash

# Run the weather data extraction script
python ../src/data/extraction/extract_weather.py
# Log the extraction
echo "$(date) Weather data extraction completed" >> ../logs/extraction.log

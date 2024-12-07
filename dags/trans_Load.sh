#!/bin/bash


# Run the weather data transformation script
/home/ubuntu/WeatherTrendsPipeline/venv/bin/python /home/ubuntu/WeatherTrendsPipeline/src/data/processing/transform_weather.py
# Log the transformation
echo "$(date) Weather data transformed successfully" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log
echo "=========" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log


# Run the weather data load & delete script
/home/ubuntu/WeatherTrendsPipeline/venv/bin/python /home/ubuntu/WeatherTrendsPipeline/src/data/storage/load_weather.py
# Log the load & Delete
echo "$(date) Weather data saved successfully" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log
echo "=========" >> /home/ubuntu/WeatherTrendsPipeline/logs/etl.log


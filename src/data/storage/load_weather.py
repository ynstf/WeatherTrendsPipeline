import os
import time
from dotenv import load_dotenv
from pathlib import Path
import sys

time.sleep(10)

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(project_root)

from src.utils.save_data import load_weather_data, save_weather_data_to_url

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
date = time.strftime("%Y%m%d")
path_raw_data = os.path.join(project_root, "data", "raw", "weather_data.csv")
path = os.path.join(project_root, "data", "processed", "weather_data_processed.csv")

try:
    # Load the data
    data = load_weather_data(path)
    
    # Set up AWS credentials (without token)
    aws_credentials = {
        "key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret": os.getenv("AWS_SECRET_ACCESS_KEY")
    }
    
    # Save to S3
    s3_path = f"s3://{BUCKET_NAME}/weather_data_{date}.csv"
    save_weather_data_to_url(data, s3_path, aws_credentials)
    print(f"Data saved successfully to {s3_path}")
    
    # Delete the local file after successful upload
    if os.path.exists(path):
        os.remove(path)
        os.remove(path_raw_data)
        print(f"Successfully deleted local files: {path} , {path_raw_data}")

except Exception as e:
    print(f"Error occurred: {str(e)}")

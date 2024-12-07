import pandas as pd
import time
import os
from dotenv import load_dotenv

def load_weather_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def save_weather_data_to_url(df: pd.DataFrame, url: str, storage_options: dict) -> None:
    import boto3
    from urllib.parse import urlparse
    
    # Parse the S3 URL
    parsed_url = urlparse(url)
    bucket_name = parsed_url.netloc
    key = parsed_url.path.lstrip('/')
    
    # Create a temporary CSV file
    temp_file = "temp_weather_data.csv"
    df.to_csv(temp_file, index=False)
    
    # Initialize S3 client with only access key and secret key
    s3_client = boto3.client(
        's3',
        aws_access_key_id=storage_options['key'],
        aws_secret_access_key=storage_options['secret']
    )
    
    # Upload the file
    try:
        s3_client.upload_file(temp_file, bucket_name, key)
        os.remove(temp_file)  # Clean up temporary file
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)  # Clean up temporary file even if upload fails
        raise e
        
"""
if __name__ == "__main__":
    load_dotenv()
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    date =  time.strftime("%Y%m%d")
    path = "data/processed/weather_data_processed.csv"
    data = load_weather_data(path)
    AWS_TOKEN = os.getenv("AWS_TOKEN")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    aws_credentials = {
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY,
        "token": AWS_TOKEN
    }

    save_weather_data_to_url(data, f"s3://{BUCKET_NAME}/{date}/weather_data.csv", aws_credentials)
    print(f"Data saved successfully to s3://{BUCKET_NAME}/{date}/weather_data.csv")
"""
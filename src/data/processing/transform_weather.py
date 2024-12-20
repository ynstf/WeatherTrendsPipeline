import os
import sys
from pathlib import Path

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(project_root)

from src.utils.def_transformations import process_weather_data

if __name__ == "__main__":
    # Define input and output paths
    input_file = os.path.join(project_root, "data", "raw", "weather_data.csv")
    output_file = os.path.join(project_root, "data", "processed", "weather_data_processed.csv")
    
    try:
        # Process the weather data
        processed_df = process_weather_data(input_file, output_file)
        print("Data processing complete. Check the output file for results.")
    except Exception as e:
        print(f"Error processing weather data: {str(e)}")

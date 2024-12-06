import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Union, Optional

def load_weather_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load weather data from CSV file"""
    return pd.read_csv(file_path)

def fahrenheit_to_celsius(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Convert temperature from Fahrenheit to Celsius"""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[f'{col}_celsius'] = (df[col] - 32) * 5/9
    return df

def convert_wind_speed(df: pd.DataFrame, from_unit: str = 'mph', to_unit: str = 'kmh') -> pd.DataFrame:
    """Convert wind speed between different units"""
    df = df.copy()
    if 'wind_speed' not in df.columns:
        return df
        
    if from_unit == 'mph' and to_unit == 'kmh':
        df['wind_speed_kmh'] = df['wind_speed'] * 1.60934
    elif from_unit == 'mph' and to_unit == 'ms':
        df['wind_speed_ms'] = df['wind_speed'] * 0.44704
    elif from_unit == 'ms' and to_unit == 'kmh':
        df['wind_speed_kmh'] = df['wind_speed'] * 3.6
        
    return df

def convert_pressure(df: pd.DataFrame, from_unit: str = 'mb', to_unit: str = 'hpa') -> pd.DataFrame:
    """Convert pressure between different units"""
    df = df.copy()
    if 'pressure' not in df.columns:
        return df
        
    if from_unit == 'mb' and to_unit == 'hpa':
        df['pressure_hpa'] = df['pressure']
    elif from_unit == 'mb' and to_unit == 'atm':
        df['pressure_atm'] = df['pressure'] / 1013.25
        
    return df

def convert_visibility(df: pd.DataFrame, from_unit: str = 'miles', to_unit: str = 'km') -> pd.DataFrame:
    """Convert visibility distance"""
    df = df.copy()
    if 'visibility' not in df.columns:
        return df
        
    if from_unit == 'miles' and to_unit == 'km':
        df['visibility_km'] = df['visibility'] * 1.60934
        
    return df

def process_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """Process timestamp column to extract useful time components"""
    df = df.copy()
    if 'timestamp' not in df.columns:
        return df
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['month'] = df['timestamp'].dt.month_name()
    df['season'] = df['timestamp'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    
    return df

def calculate_heat_index(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate heat index using temperature and humidity"""
    df = df.copy()
    if 'temperature' not in df.columns or 'humidity' not in df.columns:
        return df
    
    mask = df['temperature'] >= 80
    
    c1, c2, c3 = -42.379, 2.04901523, 10.14333127
    c4, c5, c6 = -0.22475541, -6.83783e-3, -5.481717e-2
    c7, c8, c9 = 1.22874e-3, 8.5282e-4, -1.99e-6
    
    T = df.loc[mask, 'temperature']
    RH = df.loc[mask, 'humidity']
    
    df.loc[mask, 'heat_index'] = (
        c1 + c2*T + c3*RH + c4*T*RH + c5*T**2 + c6*RH**2 + 
        c7*T**2*RH + c8*T*RH**2 + c9*T**2*RH**2
    )
    
    df.loc[~mask, 'heat_index'] = df.loc[~mask, 'temperature']
    return df

def calculate_wind_chill(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate wind chill temperature"""
    df = df.copy()
    if 'temperature' not in df.columns or 'wind_speed' not in df.columns:
        return df
    
    mask = (df['temperature'] <= 50) & (df['wind_speed'] > 3)
    T = df.loc[mask, 'temperature']
    V = df.loc[mask, 'wind_speed']
    
    df.loc[mask, 'wind_chill'] = (
        35.74 + 0.6215*T - 35.75*V**0.16 + 0.4275*T*V**0.16
    )
    
    df.loc[~mask, 'wind_chill'] = df.loc[~mask, 'temperature']
    return df

def process_weather_data(input_file: Union[str, Path], output_file: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Process weather data with all available transformations"""
    df = load_weather_data(input_file)
    
    df = fahrenheit_to_celsius(df, ['temperature', 'apparent_temperature', 'dew_point'])
    df = convert_wind_speed(df, from_unit='mph', to_unit='kmh')
    df = convert_pressure(df, from_unit='mb', to_unit='hpa')
    df = convert_visibility(df, from_unit='miles', to_unit='km')
    df = process_timestamps(df)
    df = calculate_heat_index(df)
    df = calculate_wind_chill(df)
    
    if output_file:
        df.to_csv(output_file, index=False)
        
    return df

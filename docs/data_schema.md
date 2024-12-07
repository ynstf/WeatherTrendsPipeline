# Data Schema Documentation

## Raw Data Schema

### Weather Data (CSV)
| Column Name   | Data Type | Description                    | Units      |
|--------------|-----------|--------------------------------|------------|
| timestamp    | datetime  | Time of measurement            | UTC        |
| temperature  | float     | Temperature                    | Fahrenheit |
| humidity     | integer   | Relative humidity              | %          |
| pressure     | integer   | Atmospheric pressure           | mb         |
| wind_speed   | float     | Wind speed                     | mph        |
| wind_bearing | integer   | Wind direction                 | degrees    |
| cloud_cover  | float     | Cloud coverage                 | 0-1 scale  |
| uv_index     | integer   | UV radiation index            | index      |

## Processed Data Schema

### Transformed Weather Data (CSV)
| Column Name      | Data Type | Description                    | Units      |
|-----------------|-----------|--------------------------------|------------|
| timestamp       | datetime  | Time of measurement            | UTC        |
| temperature_c   | float     | Temperature                    | Celsius    |
| humidity        | integer   | Relative humidity              | %          |
| pressure_hpa    | integer   | Atmospheric pressure           | hPa        |
| wind_speed_ms   | float     | Wind speed                     | m/s        |
| wind_bearing    | integer   | Wind direction                 | degrees    |
| cloud_cover     | float     | Cloud coverage                 | 0-1 scale  |
| uv_index        | integer   | UV radiation index            | index      |
| heat_index      | float     | Perceived temperature          | Celsius    |
| wind_chill      | float     | Wind chill temperature         | Celsius    |
| season          | string    | Season of measurement          | -          |
| hour_of_day     | integer   | Hour of measurement            | 0-23       |

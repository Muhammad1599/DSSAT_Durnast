#!/usr/bin/env python3
"""
Retrieve All Weather Variables from NASA POWER for DSSAT Simulations
====================================================================

This script retrieves all required weather variables from NASA POWER agroclimatology
service for DSSAT crop simulation models:
- Solar Radiation (SRAD): ALLSKY_SFC_SW_DWN
- Wind Speed (WIND): WS2M
- Dewpoint Temperature (DEWP): T2MDEW
- Photosynthetically Active Radiation (PAR): ALLSKY_SFC_PAR_TOT

Location: Duernast, Freising, Bayern, Germany
Coordinates: 48.403°N, 11.691°E

Author: Generated for Duernast DSSAT simulation
Date: January 2026
"""

import requests
import json
from datetime import datetime, timedelta

# Site Information
SITE_NAME = "Duernast"
LATITUDE = 48.403
LONGITUDE = 11.691

# NASA POWER API Configuration
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

def retrieve_nasa_power_weather(lat, lon, start_date, end_date):
    """
    Retrieve all weather variables from NASA POWER API
    
    Parameters:
    -----------
    lat : float
        Latitude (decimal degrees)
    lon : float
        Longitude (decimal degrees)
    start_date : str
        Start date in YYYYMMDD format (e.g., "20150101")
    end_date : str
        End date in YYYYMMDD format (e.g., "20151231")
        
    Returns:
    --------
    dict : Daily weather data {YYYYMMDD: {SRAD: value, WIND: value, DEWP: value, PAR: value}}
    """
    
    print(f"\n{'='*80}")
    print(f"RETRIEVING NASA POWER WEATHER DATA")
    print(f"{'='*80}")
    print(f"\nSite: {SITE_NAME}")
    print(f"Location: {lat}°N, {lon}°E")
    print(f"Date Range: {start_date} to {end_date}")
    print(f"\nParameters:")
    print(f"  - SRAD: ALLSKY_SFC_SW_DWN (All-Sky Surface Shortwave Downward Irradiance)")
    print(f"  - WIND: WS2M (Wind Speed at 2m height)")
    print(f"  - DEWP: T2MDEW (Dewpoint Temperature at 2m)")
    print(f"  - PAR:  ALLSKY_SFC_PAR_TOT (All-Sky Surface PAR Total)")
    
    # API Parameters - retrieve all variables in one request
    params = {
        'parameters': 'ALLSKY_SFC_SW_DWN,WS2M,T2MDEW,ALLSKY_SFC_PAR_TOT',
        'community': 'AG',  # Agricultural community
        'longitude': lon,
        'latitude': lat,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }
    
    print(f"\nContacting NASA POWER API...")
    print(f"URL: {NASA_POWER_URL}")
    
    try:
        # Disable proxy to avoid connection issues
        session = requests.Session()
        session.trust_env = False  # Don't use proxy from environment
        response = session.get(NASA_POWER_URL, params=params, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather data
        weather_data = {}
        
        if 'properties' in data and 'parameter' in data['properties']:
            params_dict = data['properties']['parameter']
            
            # Get all dates from first parameter
            first_param = list(params_dict.keys())[0]
            dates = list(params_dict[first_param].keys())
            
            for date_str in dates:
                weather_data[date_str] = {}
                
                # Extract SRAD (MJ/m²/day) - already in correct units
                srad_value = params_dict.get('ALLSKY_SFC_SW_DWN', {}).get(date_str, -999)
                if srad_value is not None and srad_value != -999:
                    weather_data[date_str]['SRAD'] = round(float(srad_value), 2)
                else:
                    weather_data[date_str]['SRAD'] = -99.0
                
                # Extract WIND (m/s) - convert to km/day
                wind_ms = params_dict.get('WS2M', {}).get(date_str, -999)
                if wind_ms is not None and wind_ms != -999:
                    # Convert m/s to km/day: m/s * 86400 s/day / 1000 m/km = m/s * 86.4
                    wind_km_day = float(wind_ms) * 86.4
                    weather_data[date_str]['WIND'] = round(wind_km_day, 1)
                else:
                    weather_data[date_str]['WIND'] = -99.0
                
                # Extract DEWP (°C) - already in correct units
                dewp_value = params_dict.get('T2MDEW', {}).get(date_str, -999)
                if dewp_value is not None and dewp_value != -999:
                    weather_data[date_str]['DEWP'] = round(float(dewp_value), 1)
                else:
                    weather_data[date_str]['DEWP'] = -99.0
                
                # Extract PAR (mol/m²/day) - already in correct units
                par_value = params_dict.get('ALLSKY_SFC_PAR_TOT', {}).get(date_str, -999)
                if par_value is not None and par_value != -999:
                    weather_data[date_str]['PAR'] = round(float(par_value), 2)
                else:
                    weather_data[date_str]['PAR'] = -99.0
            
            print(f"\n[SUCCESS] Retrieved {len(weather_data)} days of weather data")
            
            # Statistics
            print(f"\n{'='*80}")
            print(f"DATA QUALITY SUMMARY")
            print(f"{'='*80}")
            
            # SRAD statistics
            srad_values = [d['SRAD'] for d in weather_data.values() if d['SRAD'] > 0]
            if srad_values:
                print(f"\nSolar Radiation (SRAD):")
                print(f"  Valid records: {len(srad_values)}/{len(weather_data)} days")
                print(f"  Mean: {sum(srad_values)/len(srad_values):.2f} MJ/m²/day")
                print(f"  Min:  {min(srad_values):.2f} MJ/m²/day")
                print(f"  Max:  {max(srad_values):.2f} MJ/m²/day")
            
            # WIND statistics
            wind_values = [d['WIND'] for d in weather_data.values() if d['WIND'] > 0]
            if wind_values:
                print(f"\nWind Speed (WIND):")
                print(f"  Valid records: {len(wind_values)}/{len(weather_data)} days")
                print(f"  Mean: {sum(wind_values)/len(wind_values):.1f} km/day")
                print(f"  Min:  {min(wind_values):.1f} km/day")
                print(f"  Max:  {max(wind_values):.1f} km/day")
            
            # DEWP statistics
            dewp_values = [d['DEWP'] for d in weather_data.values() if d['DEWP'] != -99.0]
            if dewp_values:
                print(f"\nDewpoint Temperature (DEWP):")
                print(f"  Valid records: {len(dewp_values)}/{len(weather_data)} days")
                print(f"  Mean: {sum(dewp_values)/len(dewp_values):.1f} °C")
                print(f"  Min:  {min(dewp_values):.1f} °C")
                print(f"  Max:  {max(dewp_values):.1f} °C")
            
            # PAR statistics
            par_values = [d['PAR'] for d in weather_data.values() if d['PAR'] > 0]
            if par_values:
                print(f"\nPhotosynthetically Active Radiation (PAR):")
                print(f"  Valid records: {len(par_values)}/{len(weather_data)} days")
                print(f"  Mean: {sum(par_values)/len(par_values):.2f} mol/m²/day")
                print(f"  Min:  {min(par_values):.2f} mol/m²/day")
                print(f"  Max:  {max(par_values):.2f} mol/m²/day")
            
            return weather_data
            
        else:
            print("[ERROR] Unexpected data format from NASA POWER API")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download data: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error processing data: {e}")
        return None


def convert_to_dssat_date(yyyymmdd_str):
    """
    Convert YYYYMMDD date string to DSSAT YYDDD format
    
    Parameters:
    -----------
    yyyymmdd_str : str
        Date in YYYYMMDD format (e.g., "20150101")
        
    Returns:
    --------
    int
        DSSAT date code in YYDDD format (e.g., 15001)
    """
    year = int(yyyymmdd_str[:4])
    month = int(yyyymmdd_str[4:6])
    day = int(yyyymmdd_str[6:8])
    
    date_obj = datetime(year, month, day)
    day_of_year = date_obj.timetuple().tm_yday
    year_short = year % 100
    
    return int(f"{year_short:02d}{day_of_year:03d}")


if __name__ == "__main__":
    """
    Example usage: Retrieve weather data for 2015
    """
    
    # Example: 2015 data
    start_date = "20150101"
    end_date = "20151231"
    
    print("\n" + "="*80)
    print("EXAMPLE: Retrieving 2015 Weather Data")
    print("="*80)
    
    weather_data = retrieve_nasa_power_weather(
        LATITUDE, 
        LONGITUDE, 
        start_date, 
        end_date
    )
    
    if weather_data:
        # Show sample of first few days
        print(f"\n{'='*80}")
        print(f"SAMPLE DATA (First 5 days)")
        print(f"{'='*80}")
        print(f"\n{'Date':<12} {'SRAD':<10} {'WIND':<10} {'DEWP':<10} {'PAR':<10}")
        print("-" * 60)
        
        for i, (date_str, values) in enumerate(sorted(weather_data.items())[:5]):
            dssat_date = convert_to_dssat_date(date_str)
            print(f"{date_str} ({dssat_date})  "
                  f"{values['SRAD']:<10.2f} "
                  f"{values['WIND']:<10.1f} "
                  f"{values['DEWP']:<10.1f} "
                  f"{values['PAR']:<10.2f}")
        
        print(f"\n[SUCCESS] Retrieved {len(weather_data)} days of complete weather data")
        print(f"\nNote: This script retrieves all variables in a single API call for efficiency.")
        print(f"      The data can be integrated into DSSAT weather files using appropriate")
        print(f"      formatting functions to maintain fixed-width column alignment.")

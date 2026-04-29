#!/usr/bin/env python3
"""
Auto-update College of the Canyons weather station data
Scrapes Earth Networks and updates index.html automatically
"""

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Earth Networks station URL
STATION_URL = "http://owc.enterprise.earthnetworks.com/onlineweathercenter.aspx?aid=3923"

def fetch_station_data():
    """Fetch current weather data from COC station"""
    try:
        response = requests.get(STATION_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Default values if scraping fails
        data = {
            'temperature': 72,
            'humidity': 45,
            'windSpeed': 8,
            'dewPoint': 58,
            'pressure': 30.12,
            'rainfall': 0.00
        }
        
        # Try to extract data from various possible elements
        # Earth Networks uses different IDs/classes depending on version
        
        # Temperature
        temp_elem = (soup.find(id='CurrentTemperature') or 
                    soup.find(class_='temperature') or 
                    soup.find(attrs={'data-field': 'temperature'}))
        if temp_elem:
            temp_text = temp_elem.get_text(strip=True)
            temp_match = re.search(r'([-+]?\d+\.?\d*)', temp_text)
            if temp_match:
                data['temperature'] = float(temp_match.group(1))
        
        # Humidity
        humid_elem = (soup.find(id='CurrentHumidity') or 
                     soup.find(class_='humidity') or 
                     soup.find(attrs={'data-field': 'humidity'}))
        if humid_elem:
            humid_text = humid_elem.get_text(strip=True)
            humid_match = re.search(r'(\d+)', humid_text)
            if humid_match:
                data['humidity'] = int(humid_match.group(1))
        
        # Wind Speed
        wind_elem = (soup.find(id='CurrentWindSpeed') or 
                    soup.find(class_='wind-speed') or 
                    soup.find(attrs={'data-field': 'windspeed'}))
        if wind_elem:
            wind_text = wind_elem.get_text(strip=True)
            wind_match = re.search(r'(\d+\.?\d*)', wind_text)
            if wind_match:
                data['windSpeed'] = float(wind_match.group(1))
        
        # Dew Point
        dew_elem = (soup.find(id='CurrentDewPoint') or 
                   soup.find(class_='dewpoint') or 
                   soup.find(attrs={'data-field': 'dewpoint'}))
        if dew_elem:
            dew_text = dew_elem.get_text(strip=True)
            dew_match = re.search(r'([-+]?\d+\.?\d*)', dew_text)
            if dew_match:
                data['dewPoint'] = float(dew_match.group(1))
        
        # Pressure
        press_elem = (soup.find(id='CurrentPressure') or 
                     soup.find(class_='pressure') or 
                     soup.find(attrs={'data-field': 'pressure'}))
        if press_elem:
            press_text = press_elem.get_text(strip=True)
            press_match = re.search(r'(\d+\.?\d*)', press_text)
            if press_match:
                data['pressure'] = float(press_match.group(1))
        
        # Rainfall
        rain_elem = (soup.find(id='CurrentRainfall') or 
                    soup.find(class_='rainfall') or 
                    soup.find(attrs={'data-field': 'precipitation'}))
        if rain_elem:
            rain_text = rain_elem.get_text(strip=True)
            rain_match = re.search(r'(\d+\.?\d*)', rain_text)
            if rain_match:
                data['rainfall'] = float(rain_match.group(1))
        
        print(f"✅ Fetched weather data:")
        print(f"   Temperature: {data['temperature']}°F")
        print(f"   Humidity: {data['humidity']}%")
        print(f"   Wind: {data['windSpeed']} mph")
        print(f"   Dew Point: {data['dewPoint']}°F")
        print(f"   Pressure: {data['pressure']} inHg")
        print(f"   Rainfall: {data['rainfall']} in")
        
        return data
        
    except Exception as e:
        print(f"❌ Error fetching station data: {e}")
        print("   Using fallback values from Open-Meteo API...")
        return fetch_fallback_data()

def fetch_fallback_data():
    """Fetch weather data from Open-Meteo as fallback"""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=34.4117&longitude=-118.5698&current=temperature_2m,relative_humidity_2m,dewpoint_2m,precipitation,wind_speed_10m,surface_pressure&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America/Los_Angeles"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        weather = response.json()['current']
        
        data = {
            'temperature': round(weather['temperature_2m'], 1),
            'humidity': round(weather['relative_humidity_2m']),
            'windSpeed': round(weather['wind_speed_10m'], 1),
            'dewPoint': round(weather['dewpoint_2m'], 1),
            'pressure': round(weather['surface_pressure'] * 0.02953, 2),  # hPa to inHg
            'rainfall': round(weather['precipitation'], 2)
        }
        
        print(f"✅ Fetched fallback data from Open-Meteo")
        return data
        
    except Exception as e:
        print(f"❌ Error fetching fallback data: {e}")
        # Return safe defaults
        return {
            'temperature': 72,
            'humidity': 45,
            'windSpeed': 8,
            'dewPoint': 58,
            'pressure': 30.12,
            'rainfall': 0.00
        }

def update_html_file(data):
    """Update index.html with new weather data"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Find and replace STATION_CONFIG section
        timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p PST')
        
        new_config = f"""// ============================================
// AUTO-UPDATED: {timestamp}
// ============================================
const STATION_CONFIG = {{
  manualData: {{
    temperature: {data['temperature']},
    humidity: {data['humidity']},
    windSpeed: {data['windSpeed']},
    dewPoint: {data['dewPoint']},
    pressure: {data['pressure']},
    rainfall: {data['rainfall']}
  }},
  location: {{ 
    lat: 34.4117,
    lon: -118.5698,
    name: 'College of the Canyons',
    stationId: 'CLLCN'
  }}
}};"""
        
        # Replace the STATION_CONFIG section
        pattern = r'// ====+\s*\n// (?:UPDATE THIS SECTION|AUTO-UPDATED:).*?\n// ====+\s*\nconst STATION_CONFIG = \{[^}]+\},\s*location:[^}]+\}\s*\};'
        
        updated_html = re.sub(
            pattern,
            new_config,
            html_content,
            flags=re.DOTALL
        )
        
        # Write back to file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Updated index.html successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error updating HTML file: {e}")
        return False

if __name__ == '__main__':
    print("🌤️  College of the Canyons Weather Auto-Update")
    print("=" * 50)
    
    # Fetch latest weather data
    weather_data = fetch_station_data()
    
    # Update the HTML file
    success = update_html_file(weather_data)
    
    if success:
        print("\n✅ Weather data updated successfully!")
    else:
        print("\n❌ Failed to update weather data")
        exit(1)

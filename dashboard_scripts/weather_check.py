#!/usr/bin/env python3
"""
Weather Check Script
Get current weather information for specified locations
"""

import requests
import json
import sys
import os
from datetime import datetime

class WeatherChecker:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'weather_config.json')
        self.load_config()

    def load_config(self):
        """Load weather configuration"""
        default_config = {
            "api_key": "",
            "default_locations": [
                {"name": "New York", "country": "US"},
                {"name": "London", "country": "GB"},
                {"name": "Tokyo", "country": "JP"}
            ],
            "units": "metric",  # metric, imperial, or kelvin
            "language": "en"
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
                self.save_config()
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def get_weather_free(self, location):
        """Get weather using free service (wttr.in)"""
        try:
            # Use wttr.in service (no API key required)
            url = f"http://wttr.in/{location}?format=j1"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self.parse_wttr_data(data, location)
            else:
                return None

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def parse_wttr_data(self, data, location):
        """Parse wttr.in weather data"""
        try:
            current = data['current_condition'][0]
            weather = data['weather'][0]

            # Get current conditions
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            humidity = current['humidity']
            pressure = current['pressure']
            visibility = current['visibility']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            description = current['weatherDesc'][0]['value']
            feels_like_c = current['FeelsLikeC']
            feels_like_f = current['FeelsLikeF']

            # Get today's forecast
            min_temp_c = weather['mintempC']
            max_temp_c = weather['maxtempC']
            min_temp_f = weather['mintempF']
            max_temp_f = weather['maxtempF']

            return {
                'location': location,
                'description': description,
                'temperature': {'celsius': int(temp_c), 'fahrenheit': int(temp_f)},
                'feels_like': {'celsius': int(feels_like_c), 'fahrenheit': int(feels_like_f)},
                'humidity': int(humidity),
                'pressure': int(pressure),
                'visibility': int(visibility),
                'wind': {'speed': int(wind_speed), 'direction': wind_dir},
                'forecast': {
                    'min_temp': {'celsius': int(min_temp_c), 'fahrenheit': int(min_temp_f)},
                    'max_temp': {'celsius': int(max_temp_c), 'fahrenheit': int(max_temp_f)}
                }
            }

        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None

    def display_weather(self, weather_data):
        """Display weather information"""
        if not weather_data:
            print("❌ No weather data available")
            return

        # Weather emoji mapping
        weather_emojis = {
            'sunny': '☀️', 'clear': '☀️',
            'partly cloudy': '⛅', 'cloudy': '☁️',
            'overcast': '☁️', 'mist': '🌫️',
            'fog': '🌫️', 'rain': '🌧️',
            'drizzle': '🌦️', 'shower': '🌦️',
            'thunderstorm': '⛈️', 'snow': '❄️',
            'sleet': '🌨️', 'wind': '💨'
        }

        # Find appropriate emoji
        description_lower = weather_data['description'].lower()
        emoji = '🌤️'  # default
        for key, value in weather_emojis.items():
            if key in description_lower:
                emoji = value
                break

        print(f"\n{emoji} WEATHER FOR {weather_data['location'].upper()}")
        print("=" * 40)

        # Current conditions
        temp_c = weather_data['temperature']['celsius']
        temp_f = weather_data['temperature']['fahrenheit']
        feels_c = weather_data['feels_like']['celsius']
        feels_f = weather_data['feels_like']['fahrenheit']

        print(f"🌡️  Temperature: {temp_c}°C ({temp_f}°F)")
        print(f"🤚 Feels like: {feels_c}°C ({feels_f}°F)")
        print(f"☁️  Conditions: {weather_data['description']}")
        print(f"💧 Humidity: {weather_data['humidity']}%")
        print(f"📊 Pressure: {weather_data['pressure']} hPa")
        print(f"👁️  Visibility: {weather_data['visibility']} km")
        print(f"💨 Wind: {weather_data['wind']['speed']} km/h {weather_data['wind']['direction']}")

        # Today's forecast
        min_c = weather_data['forecast']['min_temp']['celsius']
        max_c = weather_data['forecast']['max_temp']['celsius']
        min_f = weather_data['forecast']['min_temp']['fahrenheit']
        max_f = weather_data['forecast']['max_temp']['fahrenheit']

        print(f"\n📅 Today's Range: {min_c}°C - {max_c}°C ({min_f}°F - {max_f}°F)")

    def get_weather_simple(self, location):
        """Get simple weather info using curl and wttr.in"""
        try:
            import subprocess
            cmd = f"curl -s 'wttr.in/{location}?format=3'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                return f"Weather data for {location} not available"

        except Exception as e:
            return f"Error getting weather for {location}: {e}"

    def check_multiple_locations(self):
        """Check weather for all configured locations"""
        print("🌍 WEATHER CHECK FOR MULTIPLE LOCATIONS")
        print("=" * 50)

        for location_info in self.config['default_locations']:
            location = location_info['name']
            weather_data = self.get_weather_free(location)
            self.display_weather(weather_data)
            print()

    def check_single_location(self, location):
        """Check weather for a single location"""
        weather_data = self.get_weather_free(location)
        self.display_weather(weather_data)

    def quick_weather(self, location):
        """Get quick weather summary"""
        print(f"🌤️  Quick weather for {location}:")
        simple_weather = self.get_weather_simple(location)
        print(simple_weather)

    def add_location(self, name, country=""):
        """Add a new location to default list"""
        new_location = {"name": name}
        if country:
            new_location["country"] = country

        self.config['default_locations'].append(new_location)
        self.save_config()
        print(f"✅ Added {name} to weather locations")

    def remove_location(self, name):
        """Remove a location from default list"""
        self.config['default_locations'] = [
            loc for loc in self.config['default_locations']
            if loc['name'].lower() != name.lower()
        ]
        self.save_config()
        print(f"✅ Removed {name} from weather locations")

    def list_locations(self):
        """List all configured locations"""
        print("📍 CONFIGURED WEATHER LOCATIONS")
        print("=" * 35)
        for i, location in enumerate(self.config['default_locations'], 1):
            country = location.get('country', '')
            country_str = f" ({country})" if country else ""
            print(f"{i}. {location['name']}{country_str}")

    def weather_alerts(self):
        """Check for weather alerts (simplified version)"""
        print("⚠️  WEATHER ALERTS")
        print("=" * 20)
        print("(Weather alerts require premium API access)")
        print("For severe weather alerts, check:")
        print("- National weather services")
        print("- Local emergency services")
        print("- Weather apps with alert features")

def main():
    if len(sys.argv) < 2:
        print("🌤️  Weather Checker Tool")
        print("Usage:")
        print("  python3 weather_check.py all                    - Check all configured locations")
        print("  python3 weather_check.py <location>            - Check specific location")
        print("  python3 weather_check.py quick <location>      - Quick weather summary")
        print("  python3 weather_check.py list                  - List configured locations")
        print("  python3 weather_check.py add <name> [country]  - Add location")
        print("  python3 weather_check.py remove <name>         - Remove location")
        print("  python3 weather_check.py alerts               - Weather alerts info")
        print("\nExamples:")
        print("  python3 weather_check.py 'New York'")
        print("  python3 weather_check.py quick London")
        print("  python3 weather_check.py add 'Los Angeles' US")
        return

    checker = WeatherChecker()
    command = sys.argv[1].lower()

    try:
        if command == 'all':
            checker.check_multiple_locations()
        elif command == 'quick' and len(sys.argv) >= 3:
            location = ' '.join(sys.argv[2:])
            checker.quick_weather(location)
        elif command == 'list':
            checker.list_locations()
        elif command == 'add' and len(sys.argv) >= 3:
            name = sys.argv[2]
            country = sys.argv[3] if len(sys.argv) > 3 else ""
            checker.add_location(name, country)
        elif command == 'remove' and len(sys.argv) >= 3:
            name = sys.argv[2]
            checker.remove_location(name)
        elif command == 'alerts':
            checker.weather_alerts()
        else:
            # Treat as location name
            location = ' '.join(sys.argv[1:])
            checker.check_single_location(location)

    except KeyboardInterrupt:
        print("\n\n👋 Weather check stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
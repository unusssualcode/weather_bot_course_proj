import aiohttp
from config import WEATHER_API_KEY


class WeatherAPI:
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_weather_data(data)
                    elif response.status == 404:
                        return {"error": " City not found. Check the spelling."}
                    elif response.status == 401:
                        return {
                            "error": " Invalid API key. Check WEATHER_API_KEY in .env file."
                        }
                    else:
                        return {"error": f" API error: {response.status}"}

        except aiohttp.ClientError as e:
            return {"error": f" Connection error: {str(e)}"}
        except Exception as e:
            return {"error": f" Unknown error: {str(e)}"}

    def _format_weather_data(self, data: dict) -> dict:
        try:
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
            }
            return weather_info
        except KeyError as e:
            return {"error": f"❌ Error processing data: missing field {str(e)}"}

    def format_message(self, weather_data: dict) -> str:
        if "error" in weather_data:
            return weather_data["error"]

        message = f"""
🌍 <b>{weather_data['city']}, {weather_data['country']}</b>

🌡 Temperature: <b>{weather_data['temp']}°C</b>
🤔 Feels like: <b>{weather_data['feels_like']}°C</b>
☁️ Description: <i>{weather_data['description']}</i>

💧 Humidity: {weather_data['humidity']}%
💨 Wind: {weather_data['wind_speed']} m/s
🔽 Pressure: {weather_data['pressure']} hPa
"""
        return message.strip()


weather_api = WeatherAPI()

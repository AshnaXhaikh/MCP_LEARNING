# weather_server.py

from mcp.server.fastmcp import FastMCP # Keep this line as requested
import requests
import os # Import os to check for API key in environment

# Use os.getenv() for the API key as a best practice, but keep the hardcoded key for the example
# NOTE: In a real project, replace this with os.getenv("OPENWEATHERMAP_API_KEY")
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "b97f32ed9d2f529ea2f339af0517d70c")

mcp = FastMCP("Weather")

# Helper function to get the appropriate emoji
def get_weather_emoji(description):
    """Returns an emoji based on the weather description."""
    if "rain" in description or "drizzle" in description:
        return "🌧️"
    elif "cloud" in description:
        return "☁️"
    elif "sun" in description or "clear" in description:
        return "☀️"
    elif "thunder" in description:
        return "⛈️"
    else:
        return "🌡️"

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Retrieves the current weather conditions for a specified city and returns
    a rich, formatted string for a stunning presentation.
    """
    if not API_KEY:
        return "ERROR: OPENWEATHERMAP_API_KEY is not set."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        # Improved error message for debugging
        return f"I couldn't fetch weather for {city}. Status code: {response.status_code}. Please check the city name."

    data = response.json()
    
    # Extract data for stunning output
    description = data['weather'][0]['description'].capitalize()
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    emoji = get_weather_emoji(description.lower())

    # Create the stunning, HTML-ready output string
    return (
        f"Here is the current weather in <b>{city}</b>:<br>"
        f"<ul>"
        f"<li>{emoji} <b>Condition:</b> {description}</li>"
        f"<li>🌡️ <b>Temperature:</b> {temp:.1f}°C (Feels like: {feels_like:.1f}°C)</li>"
        f"<li>💧 <b>Humidity:</b> {humidity}%</li>"
        f"<li>💨 <b>Wind Speed:</b> {wind_speed} m/s</li>"
        f"</ul>"
    )

if __name__ == "__main__":
    # Use the stable 'stdio' transport for automatic client-side management
    mcp.run(transport="stdio")
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonfiy({"error": "City parameter is required"}), 400
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Could not fetch weather data"}), response.status_code
    
    data = response.json()
    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    return jsonify(weather)

if __name__ == "__main__":
    app.run(debug=True)
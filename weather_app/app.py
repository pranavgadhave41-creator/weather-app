from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = os.getenv('WEATHER_API_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city'].strip()
        url = 'https://api.openweathermap.org/data/2.5/weather'

        response = requests.get(
            url,
            params={'q': city, 'appid': API_KEY, 'units': 'metric'},
            timeout=10
        )
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            error = "City not found. Please try again."

    return render_template('index.html', weather=weather_data, error=error)


if __name__ == '__main__':
    app.run(debug=True)